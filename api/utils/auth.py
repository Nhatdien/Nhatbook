from datetime import datetime, timedelta, timezone
import sqlalchemy.orm
from typing import Annotated, Union
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel
from api.config import settings
from api.db import database
from api.schemas.user import UserInDb, UserBase
from api.schemas.token import Token, TokenData
from api.models import models


oauth2_schemes = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash(password: str):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy() # type: ignore

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)

        id :str = payload.get("user_id") #type: ignore

        if id is None:
            raise credential_exception
        token_data = TokenData(id=id)

    except JWTError:
        raise credential_exception
    
    return token_data

def get_current_user(token: TokenData = Depends(oauth2_schemes),
                     db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Couldn't validate credential",
                                         headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token, credential_exception)  #type: ignore

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
