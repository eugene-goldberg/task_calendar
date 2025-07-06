from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, extract
import os
import uuid

from database import get_db, init_db, Event as EventModel
from config import ALLOWED_ORIGINS, ENVIRONMENT

app = FastAPI()

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()
    print(f"Running in {ENVIRONMENT} mode")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic models
class Event(BaseModel):
    id: Optional[str] = None
    title: str
    date: str
    recurrence_types: Optional[List[str]] = []  # ['daily', 'weekly', 'monthly']

class EventUpdate(BaseModel):
    title: str

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main calendar page"""
    with open("templates/index.html", "r") as f:
        return f.read()

@app.get("/api/events")
async def get_events(db: Session = Depends(get_db)):
    """Get all events organized by date"""
    events = db.query(EventModel).all()
    
    # Group events by date
    events_by_date: Dict[str, List[dict]] = {}
    for event in events:
        date_key = event.date.strftime("%Y-%m-%d")
        if date_key not in events_by_date:
            events_by_date[date_key] = []
        events_by_date[date_key].append(event.to_dict())
    
    return events_by_date

@app.get("/api/events/{date}")
async def get_events_by_date(date: str, db: Session = Depends(get_db)):
    """Get events for a specific date"""
    try:
        # Parse date string
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    # Query events for the specific date
    events = db.query(EventModel).filter(
        and_(
            extract('year', EventModel.date) == target_date.year,
            extract('month', EventModel.date) == target_date.month,
            extract('day', EventModel.date) == target_date.day
        )
    ).all()
    
    return [event.to_dict() for event in events]

@app.post("/api/events/{date}")
async def create_event(date: str, event: Event, db: Session = Depends(get_db)):
    """Create a new event with optional recurrence"""
    try:
        # Parse date string to ensure it's valid
        event_date = datetime.strptime(date, "%Y-%m-%d")
        
        # If event.date is provided, use it; otherwise use the date from URL
        if event.date:
            event_date = datetime.fromisoformat(event.date.replace('Z', '+00:00'))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    
    # Generate ID if not provided
    if not event.id:
        event.id = str(int(datetime.now().timestamp() * 1000))
    
    created_events = []
    
    # If no recurrence, create single event
    if not event.recurrence_types:
        db_event = EventModel(
            event_id=event.id,
            title=event.title,
            date=event_date
        )
        db.add(db_event)
        created_events.append(db_event)
    else:
        # Generate a group ID for all recurring events
        group_id = str(uuid.uuid4())
        
        # Track dates to avoid duplicates when multiple recurrence types are selected
        created_dates = set()
        
        # Create events for each recurrence type
        for recurrence_type in event.recurrence_types:
            # Create events for the next year
            current_date = event_date
            end_date = event_date + timedelta(days=365)
            
            while current_date <= end_date:
                # Only create event if we haven't already created one for this date
                if current_date not in created_dates:
                    # Generate unique ID for each occurrence
                    event_id = f"{event.id}_{int(current_date.timestamp() * 1000)}_{recurrence_type}"
                    
                    db_event = EventModel(
                        event_id=event_id,
                        title=event.title,
                        date=current_date,
                        recurrence_type=recurrence_type,
                        recurrence_group_id=group_id
                    )
                    db.add(db_event)
                    created_events.append(db_event)
                    created_dates.add(current_date)
                
                # Calculate next occurrence
                if recurrence_type == 'daily':
                    current_date += timedelta(days=1)
                elif recurrence_type == 'weekly':
                    current_date += timedelta(weeks=1)
                elif recurrence_type == 'monthly':
                    current_date += relativedelta(months=1)
                elif recurrence_type == 'quarterly':
                    current_date += relativedelta(months=3)
    
    try:
        db.commit()
        for event in created_events:
            db.refresh(event)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
    return {
        "message": f"Created {len(created_events)} event(s)",
        "events": [e.to_dict() for e in created_events[:10]],  # Return first 10 for preview
        "total": len(created_events)
    }

@app.put("/api/events/{date}/{event_id}")
async def update_event(date: str, event_id: str, event_update: EventUpdate, db: Session = Depends(get_db)):
    """Update an existing event"""
    # Find event by event_id
    db_event = db.query(EventModel).filter(EventModel.event_id == event_id).first()
    
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Update event
    db_event.title = event_update.title
    
    try:
        db.commit()
        db.refresh(db_event)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"message": "Event updated", "event": db_event.to_dict()}

@app.delete("/api/events/{date}/{event_id}")
async def delete_event(date: str, event_id: str, delete_all: bool = False, db: Session = Depends(get_db)):
    """Delete an event or all events in a recurrence group"""
    # Find event by event_id
    db_event = db.query(EventModel).filter(EventModel.event_id == event_id).first()
    
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    deleted_count = 0
    
    # If delete_all is True and event is part of a recurrence group, delete all
    if delete_all and db_event.recurrence_group_id:
        events_to_delete = db.query(EventModel).filter(
            EventModel.recurrence_group_id == db_event.recurrence_group_id
        ).all()
        for event in events_to_delete:
            db.delete(event)
            deleted_count += 1
    else:
        # Delete only this event
        db.delete(db_event)
        deleted_count = 1
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"message": f"Deleted {deleted_count} event(s)"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)