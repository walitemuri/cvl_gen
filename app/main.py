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
from .routers import openapi, resume, user
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

@app.get("/")
def read_root():
    return {"Hello World!"}



# @app.post("/upload/resume/")
# async def upload_resume(file: UploadFile = File(...)):
#     temp_folder = Path("temp_files")
#     temp_folder.mkdir(exist_ok=True)
#     temp_file_path = temp_folder / file.filename
#     with temp_file_path.open("wb") as buffer:
#         shutil.coptfileobj(file.file, buffer)
    
#     with open(temp_file_path, "r") as f:
#         content = f.read()
#     os.remove(temp_file_path)
#     resume = models.Resume(resume_)