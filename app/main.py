from typing import Optional
from fastapi import FastAPI, HTTPException, status, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
from pathlib import Path
from pydantic import BaseModel
import os
import openai
import dotenv
from . import models
from .database import engine
from app.schemas import GPTRequest, GPTResponse
from .routers import openapi, resume, user, auth
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

app.include_router(openapi.router)
app.include_router(resume.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"Hello World!"}
