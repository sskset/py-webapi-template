from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Subscription(Base):
    __tablename__ = 'subscription'
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    start_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
