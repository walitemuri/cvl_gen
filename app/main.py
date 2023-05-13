from typing import Optional
from fastapi import APIRouter, FastAPI, HTTPException, Request, status, File, UploadFile
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
from fastapi.responses import RedirectResponse
from fastapi.openapi.utils import get_openapi

models.Base.metadata.create_all(bind=engine)
# app = FastAPI(root_path="/api/v1", docs_url="/docs", openapi_url="/openapi.json")



app = FastAPI(docs_url="/crimsonbyte/v1/docs", redoc_url=None, openapi_url="/crimsonbyte/v1/openapi.json")
api_v1_router = APIRouter(prefix="/crimsonbyte/v1")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api_v1_router.include_router(openapi.router)
api_v1_router.include_router(resume.router)
api_v1_router.include_router(user.router)
api_v1_router.include_router(auth.router)

app.include_router(api_v1_router)

@app.get("/crimsonbyte/v1")
async def get_docs():
    return RedirectResponse(url="/crimsonbyte/v1/docs")

config = dotenv.dotenv_values(".env")
@app.get("/")
async def get_docs():
    return RedirectResponse(url="crimsonbyte/v1/docs")

