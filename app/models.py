from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base
from datetime import datetime, time

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    is_verified = Column(Boolean, default=False)
    resume_id = Column(Integer, ForeignKey('resume.id'), unique=True)

class UserAccess(Base):
    __tablename__ = "user_access"
    user_id = Column(Integer, primary_key=True, index=True)
    count = Column(Integer, default=0)
    last_accessed = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

class Resume(Base):
    __tablename__ = "resume"
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    resume_string = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
