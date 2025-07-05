from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
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
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def to_dict(self):
        """Convert event to dictionary for API response"""
        return {
            "id": self.event_id,
            "title": self.title,
            "date": self.date.isoformat()
        }

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