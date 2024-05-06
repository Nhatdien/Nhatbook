
from api.models import models
from api.db import database
from fastapi import Response, status, HTTPException, Depends, APIRouter
import typing
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import BackgroundTasks
from api.utils.send_mail import send_mail
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
from api.schemas import user
from api.utils.auth import *
from api.models.models import User


router = APIRouter(prefix="/user", tags=["User"])



@router.get("/me", response_model=user.UserResponse)
def get_user(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return current_user


@router.post("/", response_model=user.UserResponse, status_code=201)
def create_user(user: user.UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(database.get_db)):
    db_user = models.User(username=user.username, email=user.email, password=hash(user.password))
    try:
        db.add(db_user)
        background_tasks.add_task(send_mail, user.email, "Welcome to the forum", "You have successfully registered")
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    finally:
        db.commit()
        db.refresh(db_user)
        
    return db_user
    
@router.get("/{user_id}", response_model=user.UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return {"url": f"/user/{user_id}"}
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/{user_id}", response_model=user.UserResponse)
def update_user(user_id: int, user: user.UserUpdate, db: Session = Depends(database.get_db)):
    user_in_db = db.query(models.User).filter(models.User.id == user_id).first()
    if user_in_db:
        user_in_db.username = user.username
        user_in_db.email = user.email
        db.commit()
        return user_in_db
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/change_password/{user_id}")
def change_password(user_id: int, user: user.UserUpdate, db: Session = Depends(database.get_db)):
    user_in_db = db.query(models.User).filter(models.User.id == user_id).first()
    if user_in_db:
        user_in_db.password = hash(user.password)
        db.commit()
        return user_in_db
    raise HTTPException(status_code=404, detail="User not found")