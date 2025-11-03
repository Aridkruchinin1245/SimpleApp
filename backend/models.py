from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Integer, String, Column, DateTime, ForeignKey
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Base(DeclarativeBase): pass


class PostCreate(BaseModel):
    content: str = Field(min_length=10)


class CommandHandler(BaseModel):
    command: str


class nameHandler(BaseModel):
    token: str

class CommentHandler(BaseModel):
    comment: str


class RegistrationHandler(BaseModel):
    login: str = Field(min_length=3)
    age: int = Field(min=0, max=120)
    password: str = Field(min_length=5)


class AuthorisationHandler(BaseModel):
    login: str
    password: str

class Post(Base):
    __tablename__ = "Posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    author = Column(String)
    date = Column(DateTime, default=datetime.now)
    likes = Column(Integer)
    dislikes = Column(Integer)
    comments = relationship('Comment')

    def to_dict(self):
        data = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)

            if isinstance(value, datetime):
                value = value.isoformat().split('T')[0] + ' ' + value.isoformat().split('T')[1].split('.')[0]

            data[c.name] = value
        return data


class Comment(Base):
    __tablename__ = 'Comments'
    id = Column(Integer, index=True, primary_key=True)
    content = Column(String)
    date = Column(DateTime, default=datetime.now())
    post_id = Column(Integer, ForeignKey('Posts.id'))
    author = Column(String)


class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, index=True, primary_key=True)
    age = Column(Integer)
    login = Column(String)
    password = Column(String)
    author = Column(String)

