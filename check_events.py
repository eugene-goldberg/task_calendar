#!/usr/bin/env python3
"""
Check all events in the database
"""

from sqlalchemy.orm import Session
from database import engine, Event

def check_events():
    """Display all events in the database"""
    
    session = Session(engine)
    
    try:
        # Get all events ordered by date
        events = session.query(Event).order_by(Event.date).all()
        
        if not events:
            print("No events found in the database.")
            return
        
        print(f"Total events in database: {len(events)}\n")
        
        for event in events:
            print(f"Date: {event.date.strftime('%Y-%m-%d')}")
            print(f"Title: {event.title}")
            print(f"ID: {event.event_id}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error checking events: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    check_events()