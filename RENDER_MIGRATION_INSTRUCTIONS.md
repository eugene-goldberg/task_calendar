# Render Database Migration Instructions

Follow these steps to add authentication to your production calendar app on Render.

## Step 1: SSH into Render

```bash
render ssh calendar-app
```

## Step 2: Navigate to the project directory

```bash
cd /opt/render/project/src
```

## Step 3: Start Python interpreter

```bash
python3
```

## Step 4: Create the users table

Copy and paste this code into the Python interpreter:

```python
from database import Base, engine, User
from sqlalchemy import inspect

inspector = inspect(engine)
if 'users' not in inspector.get_table_names():
    User.__table__.create(engine)
    print("Users table created!")
else:
    print("Users table already exists.")
```

## Step 5: Create a production user

Copy and paste this code (but CHANGE THE USERNAME AND PASSWORD first!):

```python
from database import SessionLocal, User
from auth import get_password_hash

# IMPORTANT: Change these values!
USERNAME = "your_username"
PASSWORD = "your_secure_password"

db = SessionLocal()
try:
    existing = db.query(User).filter(User.username == USERNAME).first()
    if existing:
        print(f"User '{USERNAME}' already exists!")
    else:
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
```

## Step 6: Exit Python interpreter

```python
exit()
```

## Step 7: Test the migration

You can verify the migration worked by checking the tables:

```python
python3 -c "from database import engine; from sqlalchemy import inspect; print('Tables:', inspect(engine).get_table_names())"
```

## Important Notes

1. **Use a strong password** - Don't use simple passwords like "admin123" in production
2. **Save your credentials** - You'll need them to login to the calendar
3. **Multiple users** - You can run Step 5 multiple times with different usernames to create multiple users
4. **Security** - The password is hashed using bcrypt, so it's stored securely in the database

## Troubleshooting

If you get any import errors, make sure you're in the correct directory (`/opt/render/project/src`).

If the `auth` module is not found, you can hash the password manually:

```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash("your_password")
```

Then use `hashed_password` directly when creating the user.