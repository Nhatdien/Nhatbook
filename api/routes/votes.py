
from api.models import models
from api.db import database
from fastapi import Response, status, HTTPException, Depends, APIRouter
import typing
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
from api.schemas import vote
from api.utils.auth import *
from api.models.models import Votes


router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", response_model=vote.VoteResponse, status_code=201)
def create_vote(vote: vote.VoteCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_vote = models.Votes(vote_type=vote.vote_type, user_id=current_user.id, post_id=vote.post_id)
    delete_or_create = "created"
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        existing_vote = db.query(models.Votes).filter(models.Votes.user_id == current_user.id, models.Votes.post_id == vote.post_id).first()
        # if the user has already voted on the post, delete the vote, else add the vote
        if existing_vote:
            if existing_vote.vote_type == vote.vote_type and existing_vote.post_id == vote.post_id and existing_vote.user_id == current_user.id:
                db.delete(existing_vote)
                delete_or_create = "deleted"
            elif existing_vote.vote_type != vote.vote_type and existing_vote.post_id == vote.post_id and existing_vote.user_id == current_user.id:
                delete_or_create = "updated"
                existing_vote.vote_type = vote.vote_type
        else:
            db.add(db_vote)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=e)
    finally:
        db.commit()
        
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": f"Vote {delete_or_create}"})


@router.get("/{post_id}", response_model=typing.List[vote.VoteResponse])
def get_vote_by_post_id(post_id: int, db: Session = Depends(database.get_db)):
    #a post can have multiple votes, so get all votes for a post
    votes = db.query(models.Votes).filter(models.Votes.post_id == post_id).all()
    if votes:
        return votes
    raise HTTPException(status_code=404, detail="Vote not found")