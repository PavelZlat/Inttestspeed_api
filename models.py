from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class SpeedTestResult(Base):
    __tablename__ = "speed_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    download_speed = Column(Float)
    upload_speed = Column(Float)
    ping = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)