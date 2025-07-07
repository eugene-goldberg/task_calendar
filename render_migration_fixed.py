"""
Fixed migration script for Render - works without passlib.
Copy this entire file to Render shell and run it.
"""

# Step 1: Create the users table
print("Step 1: Creating users table...")
print("-" * 50)

from database import engine, SessionLocal
from sqlalchemy import text

try:
    # Create users table using raw SQL
    engine.execute(text("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        hashed_password VARCHAR(255) NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE
    )
    """))
    print("✓ Users table created successfully!")
except Exception as e:
    print(f"✗ Error creating table: {str(e)}")
    print("  (Table might already exist, continuing...)")

# Step 2: Create a user with pre-hashed password
print("\nStep 2: Creating user...")
print("-" * 50)

# User credentials with pre-generated hash
USERNAME = "-DZ-"
# This is the bcrypt hash for "@DZAdmin42!"
HASHED_PASSWORD = "$2b$12$wNfEMS7nIGj.yk7nPrj.1.SMmzqu/gwE0jqhTec9O7k1jydooz4eu"

db = SessionLocal()
try:
    # Check if user already exists
    result = db.execute(text("SELECT username FROM users WHERE username = :u"), {"u": USERNAME})
    existing_user = result.fetchone()
    
    if existing_user:
        print(f"✗ User '{USERNAME}' already exists!")
    else:
        # Create the user
        db.execute(
            text("INSERT INTO users (username, hashed_password, is_active) VALUES (:u, :p, true)"),
            {"u": USERNAME, "p": HASHED_PASSWORD}
        )
        db.commit()
        print(f"✓ User '{USERNAME}' created successfully!")
        print(f"\nYou can now login with:")
        print(f"  Username: {USERNAME}")
        print(f"  Password: @DZAdmin42!")
except Exception as e:
    db.rollback()
    print(f"✗ Error creating user: {str(e)}")
finally:
    db.close()

# Step 3: Verify the migration
print("\nStep 3: Verifying migration...")
print("-" * 50)

db = SessionLocal()
try:
    # Check tables
    result = db.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
    tables = [row[0] for row in result]
    print(f"✓ Database tables: {', '.join(tables)}")
    
    # Check users
    result = db.execute(text("SELECT username, is_active FROM users"))
    users = result.fetchall()
    print(f"✓ Users in database: {len(users)}")
    for user in users:
        print(f"  - {user[0]} (active: {user[1]})")
except Exception as e:
    print(f"✗ Error verifying: {str(e)}")
finally:
    db.close()

print("\n" + "=" * 50)
print("Migration completed!")
print("\nNext steps:")
print("1. Deploy your latest code through Render dashboard")
print("2. Access your calendar app")
print("3. Login with the credentials created above")
print("=" * 50)