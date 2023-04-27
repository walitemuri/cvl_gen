from typing import List, Optional
from pydantic import BaseModel, EmailStr


class GPTRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 1500
    n: Optional[int] = 1
    stop: Optional[str] = None
    temperature: Optional[float] = 1.0
    
    
class GPTResponse(BaseModel):
    response: str
    
    
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