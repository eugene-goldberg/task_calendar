#!/usr/bin/env python3
"""Create a test user for the calendar application"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import get_db, User, SessionLocal
from auth import get_password_hash

def create_test_user():
    """Create a test user"""
    # Default test credentials
    username = "admin"
    password = "admin123"
    
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            print(f"User '{username}' already exists!")
            return
        
        # Create new user
        hashed_password = get_password_hash(password)
        new_user = User(
            username=username,
            hashed_password=hashed_password,
            is_active=True
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print(f"Test user created successfully!")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print("\nIMPORTANT: Please change this password for production use!")
        
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()