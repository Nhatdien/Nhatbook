
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
    
@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{user_id}", response_model=UrlResponse)
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        return {"url": f"/user/{user_id}"}
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: user.UserUpdate, db: Session = Depends(database.get_db)):
    user_in_db = db.query(models.User).filter(models.User.id == user_id).first()
    if user_in_db:
        user_in_db.username = user.username
        user_in_db.email = user.email
        db.commit()
        return user_in_db
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/change_password/{user_id}", response_model=UserResponse)
def change_password(user_id: int, user: user.UserUpdate, db: Session = Depends(database.get_db)):
    user_in_db = db.query(models.User).filter(models.User.id == user_id).first()
    if user_in_db:
        user_in_db.password = hash(user.password)
        db.commit()
        return user_in_db
    raise HTTPException(status_code=404, detail="User not found")