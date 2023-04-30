

from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
import openai
import dotenv
from app.schemas import GPTRequest, GPTResponse, Content
from .. import oauth2

config = dotenv.dotenv_values(".env")
openai.api_key = config['OPENAI_API_KEY']

router = APIRouter(tags=["OpenAI API Requests"])


@router.post("/generate", status_code=status.HTTP_200_OK, response_model=GPTResponse)
async def generate_cvl(gpt_request: GPTRequest, current_user: int = Depends(oauth2.get_current_user)):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=gpt_request.prompt,
            max_tokens=gpt_request.max_tokens,
            n=gpt_request.n,
            stop=gpt_request.stop,
            temperature=gpt_request.temperature,
        )

        if response:
            text = response.choices[0].text
            return GPTResponse(content=Content(response=text))
        else:
            raise HTTPException(status_code=400, detail="Error making request to GPT API.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



letter_format = f"""
Limit the output to 3 concise paragraphs:

Dear [Recipient's Name],

[Opening paragraph: Introduce yourself and express interest in the position]

[Body: Explain your skills and experiences relevant to the job]

[Closing paragraph: Reiterate your interest and provide contact information]

"""