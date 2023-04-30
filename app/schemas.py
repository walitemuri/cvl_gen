from typing import List, Optional
from pydantic import BaseModel, EmailStr
from fastapi import UploadFile

class GPTRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 500
    n: Optional[int] = 1
    stop: Optional[str] = None
    temperature: Optional[float] = 1.0

class VerifyEmail(BaseModel):
    token: str
    
class ResumeUpload(BaseModel):
    resume_string: UploadFile = None
    
class Content(BaseModel):
    content: str

class GPTResponse(BaseModel):
    response: Content
    
    class Config:
        orm_mode = True
    
class JobDetails(BaseModel):
    job_description: str
    job_title: str
    role_num: str

class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    

class UserOut(BaseModel):
    id: int 
    email: EmailStr
    
    class Config:
        orm_mode = True

class ResumeOut(BaseModel):
    resume_id: int
    
    class Config:
        orm_mode = True


class CreateResume(BaseModel):
    user_id: int
    resume_string: str