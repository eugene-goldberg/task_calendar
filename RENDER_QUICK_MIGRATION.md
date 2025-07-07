# Quick Render Migration Guide

Since the User model isn't deployed yet, follow these steps:

## Option 1: Using vi editor in Render shell

1. SSH into Render:
```bash
render ssh calendar-app
```

2. Create the migration file:
```bash
cd /opt/render/project/src
vi migration.py
```

3. Press `i` to enter insert mode, then paste the content from `render_standalone_migration.py`

4. Press `ESC`, then type `:wq` to save and exit

5. Edit the file to change the username and password:
```bash
vi migration.py
# Find the lines with USERNAME and PASSWORD and change them
```

6. Run the migration:
```bash
python3 migration.py
```

## Option 2: Direct Python commands

If you prefer not to use vi, run these commands directly in Python:

1. SSH into Render and start Python:
```bash
render ssh calendar-app
cd /opt/render/project/src
python3
```

2. Create the users table:
```python
# Import required modules
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import os

# Setup
DATABASE_URL = os.getenv("DATABASE_URL")
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

# Create table
User.__table__.create(engine)
print("Users table created!")
```

3. Create a user:
```python
# Password hashing
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Set credentials (CHANGE THESE!)
USERNAME = "your_username"
PASSWORD = "your_secure_password"

# Create session
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# Create user
hashed_password = pwd_context.hash(PASSWORD)
user = User(username=USERNAME, hashed_password=hashed_password, is_active=True)
db.add(user)
db.commit()
print(f"User {USERNAME} created!")
db.close()
```

4. Exit Python:
```python
exit()
```

## After Migration

1. Deploy your latest code (with authentication features) through Render dashboard
2. Your calendar will now require login with the credentials you created

## Important Security Notes

- Use a strong password (mix of letters, numbers, symbols, 12+ characters)
- Don't use common passwords like "admin123" or "password"
- Each user should have a unique, secure password