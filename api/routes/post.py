from models import models
from db import database
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas.urls import UrlResponse
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from utils.auth import *
from models.models import Post
from schemas.post import *

router = APIRouter(prefix="/post", tags=["Post"])

@router.get("/", response_model=List[PostResponse])
def get_posts(current_user: UserInDb = Depends(get_current_user), db: Session = Depends(database.get_db)):
    if current_user.id:
        return db.query(Post).all()
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

@router.post("/", response_model=PostResponse)
def create_post(post: PostCreate, current_user: UserInDb = Depends(get_current_user), db: Session = Depends(database.get_db)):
    if current_user.id:
        create_post = models.Post(content=post.content, author_id=current_user.id)
        post.author_id = current_user.id
        db.add(create_post)
        db.commit()
        db.refresh(create_post)
        return create_post
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")