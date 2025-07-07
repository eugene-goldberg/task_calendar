#!/usr/bin/env python3
"""
Database migration script for Render production environment.
Copy and paste this entire script into the Render shell.
"""

# First, create the users table
print("Starting database migration...")
print("-" * 50)

from sqlalchemy import create_engine, Column, Integer, String, Boolean, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable not set!")
    exit(1)

# Create engine
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

# Check if table exists
inspector = inspect(engine)
if 'users' not in inspector.get_table_names():
    print("Creating users table...")
    User.__table__.create(engine)
    print("✓ Users table created successfully!")
else:
    print("✓ Users table already exists.")

# Now create a production user
print("\n" + "-" * 50)
print("Creating production user...")

from passlib.context import CryptContext

# Setup password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Get user input
print("\nEnter credentials for the production user:")
username = input("Username: ").strip()
password = input("Password: ").strip()

if not username or not password:
    print("ERROR: Username and password cannot be empty!")
    exit(1)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    # Check if user already exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        print(f"\n✗ User '{username}' already exists!")
    else:
        # Create new user
        hashed_password = pwd_context.hash(password)
        new_user = User(
            username=username,
            hashed_password=hashed_password,
            is_active=True
        )
        db.add(new_user)
        db.commit()
        print(f"\n✓ User '{username}' created successfully!")
        print("\nYou can now login to the calendar app with these credentials.")
except Exception as e:
    db.rollback()
    print(f"\n✗ Error creating user: {str(e)}")
finally:
    db.close()

print("\n" + "-" * 50)
print("Migration completed!")