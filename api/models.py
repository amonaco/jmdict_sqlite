from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class Progress(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    entry_id = Column(Integer)
    correct = Column(Integer, default=0)
    wrong = Column(Integer, default=0)

class Entry(Base):
    __tablename__ = "entry"
    id = Column(Integer, primary_key=True)
    jlpt_level = Column(String)

