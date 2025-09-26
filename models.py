from sqlalchemy import Column, Integer, String, JSON
from database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(100), nullable=False)
    user_email = Column(String(255), nullable=False, unique=True)
    age = Column(Integer)
    recommendations = Column(JSON, default=[]) 
    ZIP = Column(String(10))