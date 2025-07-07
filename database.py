from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func
from datetime import datetime
from config import DATABASE_URL

# Create engine
engine = create_engine(DATABASE_URL, echo=False)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Event model
class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event_id = Column(String(255), unique=True, index=True, nullable=False)  # Frontend ID
    title = Column(Text, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    recurrence_type = Column(String(50), nullable=True)  # 'daily', 'weekly', 'monthly', or null
    recurrence_group_id = Column(String(255), nullable=True, index=True)  # Groups recurring events together
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def to_dict(self):
        """Convert event to dictionary for API response"""
        return {
            "id": self.event_id,
            "title": self.title,
            "date": self.date.isoformat(),
            "recurrence_type": self.recurrence_type,
            "recurrence_group_id": self.recurrence_group_id
        }

# User model for authentication
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    # Create tables when run directly
    init_db()