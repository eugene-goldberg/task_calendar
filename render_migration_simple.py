"""
Simple migration script for Render shell.
Run this in the Python interpreter in Render shell.
"""

# Step 1: Import required modules
from database import Base, engine, User
from sqlalchemy import inspect

# Step 2: Check and create users table
inspector = inspect(engine)
if 'users' not in inspector.get_table_names():
    User.__table__.create(engine)
    print("Users table created!")
else:
    print("Users table already exists.")

# Step 3: Create a user (run this separately after table creation)
from database import SessionLocal, User
from auth import get_password_hash

# CHANGE THESE VALUES!
USERNAME = "admin"  # Change this to your desired username
PASSWORD = "your_secure_password_here"  # Change this to a secure password

db = SessionLocal()
try:
    # Check if user exists
    existing = db.query(User).filter(User.username == USERNAME).first()
    if existing:
        print(f"User '{USERNAME}' already exists!")
    else:
        # Create user
        user = User(
            username=USERNAME,
            hashed_password=get_password_hash(PASSWORD),
            is_active=True
        )
        db.add(user)
        db.commit()
        print(f"User '{USERNAME}' created successfully!")
except Exception as e:
    db.rollback()
    print(f"Error: {str(e)}")
finally:
    db.close()