from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import json
import os

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory storage (you can replace this with a database later)
events_storage: Dict[str, List[dict]] = {}

# Load events from file if exists (for persistence)
EVENTS_FILE = "events.json"
if os.path.exists(EVENTS_FILE):
    with open(EVENTS_FILE, "r") as f:
        events_storage = json.load(f)

def save_events_to_file():
    """Save events to file for persistence"""
    with open(EVENTS_FILE, "w") as f:
        json.dump(events_storage, f)

# Pydantic models
class Event(BaseModel):
    id: Optional[str] = None
    title: str
    date: str

class EventUpdate(BaseModel):
    title: str

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main calendar page"""
    with open("templates/index.html", "r") as f:
        return f.read()

@app.get("/api/events")
async def get_events():
    """Get all events"""
    return events_storage

@app.get("/api/events/{date}")
async def get_events_by_date(date: str):
    """Get events for a specific date"""
    return events_storage.get(date, [])

@app.post("/api/events/{date}")
async def create_event(date: str, event: Event):
    """Create a new event"""
    if date not in events_storage:
        events_storage[date] = []
    
    # Generate ID if not provided
    if not event.id:
        event.id = str(int(datetime.now().timestamp() * 1000))
    
    event_dict = event.dict()
    events_storage[date].append(event_dict)
    save_events_to_file()
    
    return {"message": "Event created", "event": event_dict}

@app.put("/api/events/{date}/{event_id}")
async def update_event(date: str, event_id: str, event_update: EventUpdate):
    """Update an existing event"""
    if date not in events_storage:
        raise HTTPException(status_code=404, detail="Date not found")
    
    for i, event in enumerate(events_storage[date]):
        if event["id"] == event_id:
            events_storage[date][i]["title"] = event_update.title
            save_events_to_file()
            return {"message": "Event updated", "event": events_storage[date][i]}
    
    raise HTTPException(status_code=404, detail="Event not found")

@app.delete("/api/events/{date}/{event_id}")
async def delete_event(date: str, event_id: str):
    """Delete an event"""
    if date not in events_storage:
        raise HTTPException(status_code=404, detail="Date not found")
    
    events_storage[date] = [e for e in events_storage[date] if e["id"] != event_id]
    
    # Remove empty date entries
    if not events_storage[date]:
        del events_storage[date]
    
    save_events_to_file()
    return {"message": "Event deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)