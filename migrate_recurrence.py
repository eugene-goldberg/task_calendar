#!/usr/bin/env python3
"""
Migration script to add recurrence columns to the events table.
"""
from sqlalchemy import text
from database import engine

def migrate():
    """Add recurrence columns to existing events table"""
    with engine.connect() as conn:
        # Check if columns already exist
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'events' 
            AND column_name IN ('recurrence_type', 'recurrence_group_id')
        """))
        
        existing_columns = [row[0] for row in result]
        
        # Add recurrence_type column if it doesn't exist
        if 'recurrence_type' not in existing_columns:
            conn.execute(text("""
                ALTER TABLE events 
                ADD COLUMN recurrence_type VARCHAR(50)
            """))
            print("Added recurrence_type column")
        
        # Add recurrence_group_id column if it doesn't exist
        if 'recurrence_group_id' not in existing_columns:
            conn.execute(text("""
                ALTER TABLE events 
                ADD COLUMN recurrence_group_id VARCHAR(255)
            """))
            # Create index for recurrence_group_id
            conn.execute(text("""
                CREATE INDEX idx_events_recurrence_group_id 
                ON events(recurrence_group_id)
            """))
            print("Added recurrence_group_id column and index")
        
        conn.commit()
        print("Migration completed successfully!")

if __name__ == "__main__":
    migrate()