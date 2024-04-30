from api.models import models
from api.db import database
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from api.utils.auth import *
from api.models.models import Post
from api.schemas.post import *

router = APIRouter(prefix="/post", tags=["Post"])

@router.get("/")
def get_posts(current_user: UserInDb = Depends(get_current_user), db: Session = Depends(database.get_db)):
    if current_user.id:
        return db.query(Post).all()
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


@router.get("/{post_id}/comments", response_model=List[PostResponse], status_code=status.HTTP_200_OK)
def get_post_comments(post_id: int, db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.replied_to_id == post_id).first()
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, current_user: UserInDb = Depends(get_current_user), db: Session = Depends(database.get_db)):
    if current_user.id:
        create_post = models.Post(content=post.content, author_id=current_user.id,  author=current_user)
        post.author_id = current_user.id
        db.add(create_post)
        db.commit()
        db.refresh(create_post)
        return create_post
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


@router.get("/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
def get_post(post_id: int, db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@router.delete("/{post_id}")
def delete_post(post_id: int, current_user: UserInDb = Depends(get_current_user), db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
        return {"url": f"/post/{post_id}"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post: PostUpdate, current_user: UserInDb = Depends(get_current_user), db: Session = Depends(database.get_db)):
    post_in_db = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post_in_db:
        post_in_db.content = post.content
        db.commit()
        return post_in_db
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@router.put("/reply/{post_id}", response_model=PostResponse)
def reply_post(post_id: int, reply: PostCreate, current_user: UserInDb = Depends(get_current_user), db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        reply_post = models.Post(content=reply.content, author_id=current_user.id, replied_to_id=post_id)
        db.add(reply_post)
        db.commit()
        db.refresh(reply_post)
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")