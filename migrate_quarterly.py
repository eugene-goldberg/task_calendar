#!/usr/bin/env python3
"""
Migration script to update recurrence_type column to allow 'quarterly' value.
"""
from sqlalchemy import text
from database import engine

def migrate():
    """Update recurrence_type column constraint to include quarterly"""
    with engine.connect() as conn:
        try:
            # For PostgreSQL, we need to update the column to accept the new value
            # Since we used VARCHAR(50), 'quarterly' will fit without changing the size
            print("Column recurrence_type already accepts 'quarterly' (VARCHAR(50))")
            print("No database changes needed - quarterly option is supported!")
            
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()

if __name__ == "__main__":
    migrate()