import api.schemas
from sqlalchemy import Column, Integer, String, Boolean,ARRAY, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from api.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(TIMESTAMP, nullable=True, server_default=text("now()"))
    updated_at = Column(TIMESTAMP, nullable=True, server_default=text("now()"), onupdate=text("now()"))

    posts = relationship("Post", back_populates="author")


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP, nullable=True, server_default=text("now"))
    updated_at = Column(TIMESTAMP, nullable=True,server_default=text("now"), onupdate=text("now()"))
    replied_to_id = Column(Integer, ForeignKey("post.id", ondelete='CASCADE'))

    author = relationship("User", back_populates="posts")

class Votes(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("post.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    vote_type = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=True, server_default=text("now()"))
    updated_at = Column(TIMESTAMP, nullable=True, server_default=text("now()"), onupdate=text("now()"))