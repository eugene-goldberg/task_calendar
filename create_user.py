#!/usr/bin/env python3
"""Create a user for the calendar application"""

import sys
import os
from getpass import getpass

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import get_db, User, SessionLocal
from auth import get_password_hash

def create_user():
    """Create a new user interactively"""
    print("Create a new user for the Calendar App")
    print("-" * 40)
    
    username = input("Username: ").strip()
    if not username:
        print("Username cannot be empty!")
        return
    
    password = getpass("Password: ")
    if not password:
        print("Password cannot be empty!")
        return
    
    confirm_password = getpass("Confirm Password: ")
    if password != confirm_password:
        print("Passwords do not match!")
        return
    
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
        
        print(f"\nUser '{username}' created successfully!")
        print("You can now login to the calendar app with these credentials.")
        
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    create_user()