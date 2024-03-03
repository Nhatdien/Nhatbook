
from models import models
from db import database
from fastapi import Response, status, HTTPException, Depends, APIRouter
import typing
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas.urls import UrlResponse
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
from schemas import user
from utils.auth import *
from models.models import User
from schemas.user import UserResponse


router = APIRouter(prefix="/user", tags=["User"])



@router.get("/me", response_model=UserBase)
def get_user(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return current_user


@router.post("/", response_model=user.UserResponse, status_code=201)
def create_user(user: user.UserCreate, db: Session = Depends(database.get_db)):
    db_user = models.User(username=user.username, email=user.email, password=hash(user.password))
    try:
        db.add(db_user)

    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    finally:
        db.commit()
        db.refresh(db_user)
        
    return db_user
    
