from api.models import models
from api.db import database
from api.service.ollama_base import OllamaBase
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from api.utils.auth import *

router = APIRouter(prefix="/ai_chat", tags=["AI Chat"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def chat(current_user: UserInDb = Depends(get_current_user), promt: str = "", db: Session = Depends(database.get_db)):
    current_ollama = OllamaBase(models="mistral", stream=False)
    current_ollama.prompt["prompt"] = promt

    if current_user.id:
       return current_ollama.post("api/generate", current_ollama.prompt)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

@router.post("/pull", status_code=status.HTTP_201_CREATED)
def pull(current_user: UserInDb = Depends(get_current_user)):
    current_ollama = OllamaBase(models="mistral", stream=False)

    if current_user.id:
       return current_ollama.pull("api/pull", "mistral")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


@router.get("/")
def get_ollama():
    current_ollama = OllamaBase(models="mistral", stream=False)

    return current_ollama.get()





   