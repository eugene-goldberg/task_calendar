# Authentication Setup

The calendar app now requires authentication to access. Here's how to set it up:

## Local Development

1. Run the migration to create the users table:
```bash
source .venv/bin/activate
python3 create_users_migration.py
```

2. Create a test user:
```bash
python3 create_test_user.py
```

This creates a default user:
- Username: `admin`
- Password: `admin123`

## Production Setup

For production on Render:

1. SSH into your Render instance:
```bash
render ssh calendar-app
```

2. Create the migration file and run it:
```python
# In the Render shell, create and run this Python script:
from database import Base, engine, User
from sqlalchemy import inspect

inspector = inspect(engine)
if 'users' not in inspector.get_table_names():
    User.__table__.create(engine)
    print("Users table created!")
```

3. Create a production user:
```python
# Create a secure user
from database import SessionLocal, User
from auth import get_password_hash

db = SessionLocal()
user = User(
    username="your_username",
    hashed_password=get_password_hash("your_secure_password"),
    is_active=True
)
db.add(user)
db.commit()
print("User created!")
```

## Usage

1. Navigate to the calendar app
2. You'll be redirected to the login page
3. Enter your credentials
4. After successful login, you'll have access to the calendar

## Security Notes

- The default test user should NEVER be used in production
- Always use strong passwords
- The JWT token expires after 30 minutes by default
- All API endpoints require authentication