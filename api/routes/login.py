from models import models
from db import database
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from schemas.urls import UrlResponse
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
from schemas.token import Token, TokenData
from utils.auth import *
from config import settings

router = APIRouter(prefix="/login", tags=["Login"])

@router.post("/", response_model=Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)
          , db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.username == user_credential.username).first()
    print(user_credential)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"user {user_credential.username} not exist")
    
    if not verify_password(user_credential.password, str(user.password)): 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credential")

    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}