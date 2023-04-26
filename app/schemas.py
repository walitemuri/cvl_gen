from typing import List, Optional
from pydantic import BaseModel


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