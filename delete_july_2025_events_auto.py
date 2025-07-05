#!/usr/bin/env python3
"""
Delete all events from July 2025 (automatic)
"""

from sqlalchemy.orm import Session
from sqlalchemy import extract, and_
from database import engine, Event

def delete_july_2025_events():
    """Delete all events from July 2025"""
    
    session = Session(engine)
    
    try:
        # Query and count July 2025 events
        july_2025_count = session.query(Event).filter(
            and_(
                extract('year', Event.date) == 2025,
                extract('month', Event.date) == 7
            )
        ).count()
        
        if july_2025_count == 0:
            print("No events found for July 2025.")
            return
        
        # Delete all July 2025 events
        deleted = session.query(Event).filter(
            and_(
                extract('year', Event.date) == 2025,
                extract('month', Event.date) == 7
            )
        ).delete()
        
        session.commit()
        print(f"Successfully deleted {deleted} events from July 2025.")
        
    except Exception as e:
        session.rollback()
        print(f"Error deleting events: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    delete_july_2025_events()