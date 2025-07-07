"""
Standalone migration script for Render - includes all necessary code.
Copy this entire file content and save it as migration.py in Render shell.
"""

# Step 1: Define the User model and create table
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import os

# Get database URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL not found!")
    exit(1)

# Create engine and base
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Check and create table
print("Checking for users table...")
inspector = inspect(engine)
if 'users' not in inspector.get_table_names():
    print("Creating users table...")
    User.__table__.create(engine)
    print("✓ Users table created successfully!")
else:
    print("✓ Users table already exists.")

# Step 2: Create a user
print("\n" + "-" * 50)
print("Now let's create a user...")
print("WARNING: Make sure to use a strong password for production!")

# Manual password hashing since auth.py might not be deployed yet
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# CHANGE THESE VALUES!
USERNAME = "-DZ-"  # <-- CHANGE THIS
PASSWORD = "@DZAdmin42!"  # <-- CHANGE THIS TO A SECURE PASSWORD

if PASSWORD == "change_me_now":
    print("\n⚠️  WARNING: You're using the default password!")
    print("Please edit this script and set a secure password before running.")
    response = input("Continue anyway? (yes/no): ")
    if response.lower() != "yes":
        print("Exiting. Please update the password and run again.")
        exit(0)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    # Check if user exists
    existing = db.query(User).filter(User.username == USERNAME).first()
    if existing:
        print(f"\n✗ User '{USERNAME}' already exists!")
    else:
        # Create user
        hashed_password = pwd_context.hash(PASSWORD)
        user = User(
            username=USERNAME,
            hashed_password=hashed_password,
            is_active=True
        )
        db.add(user)
        db.commit()
        print(f"\n✓ User '{USERNAME}' created successfully!")
        print(f"\nYou can now login with:")
        print(f"  Username: {USERNAME}")
        print(f"  Password: [the password you set]")
except Exception as e:
    db.rollback()
    print(f"\n✗ Error creating user: {str(e)}")
finally:
    db.close()

print("\n" + "-" * 50)
print("Migration completed!")
print("\nNext steps:")
print("1. Deploy your latest code with the authentication features")
print("2. Login to your calendar app with the credentials you just created")