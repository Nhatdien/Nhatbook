from sqlalchemy import Column, Integer, String, Boolean,ARRAY, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Urls(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    long_url = Column(String, index=True, nullable=False)
    short_url = Column(String, index=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("now()"), nullable=False)