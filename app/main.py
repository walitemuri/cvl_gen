from typing import Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import openai
import dotenv
from . import models
from .database import engine
from app.schemas import GPTRequest, GPTResponse

models.Base.metadata.create_all(bind=engine)
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


@app.get("/")
def read_root():
    return {"Hello World!"}

openai.api_key = config['OPENAI_API_KEY']

@app.post("/generate", status_code=status.HTTP_200_OK, response_model=GPTResponse)
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
            text = response.choices[0].text
            return GPTResponse(response=text)
        else:
            raise HTTPException(status_code=400, detail="Error making request to GPT API.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))