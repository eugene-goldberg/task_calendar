#!/usr/bin/env python3
"""
Delete all events from July 2025
"""

from sqlalchemy.orm import Session
from sqlalchemy import extract, and_
from database import engine, Event

def delete_july_2025_events():
    """Delete all events from July 2025"""
    
    session = Session(engine)
    
    try:
        # Query for July 2025 events
        july_2025_events = session.query(Event).filter(
            and_(
                extract('year', Event.date) == 2025,
                extract('month', Event.date) == 7
            )
        ).all()
        
        # Count events to be deleted
        count = len(july_2025_events)
        
        if count == 0:
            print("No events found for July 2025.")
            return
        
        # Show events that will be deleted
        print(f"Found {count} events in July 2025:")
        for event in july_2025_events:
            print(f"  - {event.date.strftime('%Y-%m-%d')}: {event.title}")
        
        # Confirm deletion
        confirm = input(f"\nAre you sure you want to delete these {count} events? (yes/no): ")
        
        if confirm.lower() == 'yes':
            # Delete the events
            for event in july_2025_events:
                session.delete(event)
            
            session.commit()
            print(f"\nSuccessfully deleted {count} events from July 2025.")
        else:
            print("\nDeletion cancelled.")
            
    except Exception as e:
        session.rollback()
        print(f"Error deleting events: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    delete_july_2025_events()