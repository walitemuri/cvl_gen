from sqlalchemy import Column, Integer, String, ForeignKey, Text, UniqueConstraint, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text(("now()")))
    is_verified = Column(Boolean, default=False)
    resume_id = Column(Integer, ForeignKey("resume.resume_id", ondelete="CASCADE"), nullable=True)
    __table_args__  = (UniqueConstraint("email", name="unique_email"),)
    
class Resume(Base):
    __tablename__ = "resume"
    
    resume_id = Column(Integer, primary_key=True, index=True, nullable=False)
    resume_string = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    __table_args__ = (UniqueConstraint('user_id', name='unique_user_resume'),)
