from pydantic import BaseModel, Field

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
