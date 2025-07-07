#!/usr/bin/env python3
"""Create a migration to add the users table"""

import os
import sys
from datetime import datetime

# Add parent directory to path to import database module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import Base, engine, User
from sqlalchemy import inspect

def create_users_table():
    """Create the users table if it doesn't exist"""
    inspector = inspect(engine)
    
    # Check if users table exists
    if 'users' not in inspector.get_table_names():
        print("Creating users table...")
        # Create only the users table
        User.__table__.create(engine)
        print("Users table created successfully!")
    else:
        print("Users table already exists.")

if __name__ == "__main__":
    create_users_table()