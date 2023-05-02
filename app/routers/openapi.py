from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
import openai
import dotenv
from app.schemas import GPTRequest, GPTResponse, Content
from sqlalchemy.orm import Session
from datetime import datetime, time
from .. import oauth2, models
from .. import database
config = dotenv.dotenv_values(".env")
openai.api_key = config['OPENAI_API_KEY']

router = APIRouter(tags=["OpenAI API Requests"])

LETTER_FORMAT = f"""
Generate a Cover Letter for a random Software Engineering position you can make up for an internship,
Limit the output to 3 concise paragraphs make it short enough that it fits on a 12 font letter sized paper Times New Roman:

"""

def update_user_access(user_id: int, db: Session):
    user = db.query(models.UserAccess).filter(models.UserAccess.user_id == user_id).first()
    if not user:
        user = models.UserAccess(user_id=user_id, count=1, last_accessed=datetime.utcnow())
        db.add(user)
        db.commit()
    else:
        if user.last_accessed.date()  < datetime.utcnow().date():
            user.count = 0
        if user.count < 3:
            user.count += 1
            user.last_accessed = datetime.utcnow()
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usage limit reached.")
    
@router.post("/generate", status_code=status.HTTP_201_CREATED, response_model=GPTResponse)
async def generate_cvl(gpt_request: GPTRequest = Depends(), current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(database.get_db)):
    resume = db.query(models.Resume).filter(models.Resume.id == current_user.id).first()
    update_user_access(current_user.id, db)
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt= LETTER_FORMAT + resume.resume_string,
            max_tokens=gpt_request.max_tokens,
            n=gpt_request.n,
            stop=gpt_request.stop,
            temperature=gpt_request.temperature,
        )

        if response:
            # print(response)
            text = response.choices[0].text
            # print(text)
            return GPTResponse(response=Content(text=text))
        else:
            raise HTTPException(status_code=400, detail="Error making request to GPT API.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

