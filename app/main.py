from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import openai
import dotenv

app = FastAPI()
origins = ["*"]

config = dotenv.dotenv_values(".env")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GPTRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 1500
    n: Optional[int] = 1
    stop: Optional[str] = None
    temperature: Optional[float] = 1.0

@app.get("/")
def read_root():
    return {"Hello World!"}

openai.api_key = config['OPENAI_API_KEY']

@app.post("/generate")
async def generate_text(gpt_request: GPTRequest):
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
            return {"choices": response.choices}
        else:
            return {"error": "Error making request to GPT API."}
    except Exception as e:
        return {"error": str(e)}
