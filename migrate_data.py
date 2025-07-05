#!/usr/bin/env python3
"""
Migrate existing events from events.json to PostgreSQL database
"""

import json
import os
from datetime import datetime
from sqlalchemy.orm import Session
from database import engine, Event, init_db

def migrate_events():
    """Migrate events from events.json to PostgreSQL"""
    
    # Initialize database
    print("Initializing database...")
    init_db()
    
    # Check if events.json exists
    if not os.path.exists("events.json"):
        print("No events.json file found. Nothing to migrate.")
        return
    
    # Load events from JSON file
    print("Loading events from events.json...")
    with open("events.json", "r") as f:
        events_data = json.load(f)
    
    if not events_data:
        print("No events found in events.json.")
        return
    
    # Create database session
    session = Session(engine)
    
    try:
        # Count total events
        total_events = sum(len(events) for events in events_data.values())
        migrated = 0
        
        print(f"Found {total_events} events to migrate...")
        
        # Migrate events
        for date_key, events in events_data.items():
            for event in events:
                # Check if event already exists
                existing = session.query(Event).filter_by(event_id=event["id"]).first()
                if existing:
                    print(f"Event {event['id']} already exists, skipping...")
                    continue
                
                # Parse date
                event_date = datetime.fromisoformat(event["date"].replace('Z', '+00:00'))
                
                # Create new event
                db_event = Event(
                    event_id=event["id"],
                    title=event["title"],
                    date=event_date
                )
                
                session.add(db_event)
                migrated += 1
                print(f"Migrated event: {event['title']} on {date_key}")
        
        # Commit changes
        session.commit()
        print(f"\nSuccessfully migrated {migrated} events to PostgreSQL!")
        
        # Optionally rename the old file
        if migrated > 0:
            os.rename("events.json", "events.json.backup")
            print("Renamed events.json to events.json.backup")
        
    except Exception as e:
        session.rollback()
        print(f"Error during migration: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    migrate_events()