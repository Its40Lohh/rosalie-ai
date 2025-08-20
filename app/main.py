from fastapi import FastAPI
import uvicorn
import redis
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(title="Rosalie AI Assistant")

# Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Database setup
DATABASE_URL = "postgresql://postgres:6474@localhost/rosalie_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    preferences = Column(Text)

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Rosalie AI Assistant is running!"}

@app.get("/test-redis")
def test_redis():
    try:
        redis_client.set("test", "Rosalie is working!")
        result = redis_client.get("test")
        return {"redis_status": "success", "message": result}
    except Exception as e:
        return {"redis_status": "error", "message": str(e)}

@app.get("/test-database")
def test_database():
    try:
        db = SessionLocal()
        # Test query - properly formatted for SQLAlchemy 2.0
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db.close()
        return {"database_status": "success", "message": "Database connection working"}
    except Exception as e:
        return {"database_status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)