from typing import List, Optional
from pydantic import BaseModel, EmailStr
from fastapi import UploadFile


class Content(BaseModel):
    text: str


class GPTRequest(BaseModel):
    max_tokens: Optional[int] = 2500
    n: Optional[int] = 1
    stop: Optional[str] = None
    temperature: Optional[float] = 1.0



class VerifyEmail(BaseModel):
    token: str


class ResumeUpload(BaseModel):
    resume_string: UploadFile = None


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
    scopes: List[str] = []


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class ResumeOut(BaseModel):
    id: int

    class Config:
        orm_mode = True


class CreateResume(BaseModel):
    resume_string: str


class ResumeRequest(BaseModel):
    resume_string: str

    class Config:
        orm_mode = True
