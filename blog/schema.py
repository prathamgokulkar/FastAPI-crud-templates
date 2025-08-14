from pydantic import BaseModel
from typing import Optional

class BlogPost(BaseModel):
    title: str
    content: str
    user_id: int
    class Config:
        orm_mode = True

class User(BaseModel):
    username: str
    email: str
    password: str
    class Config:
        orm_mode = True

class ShowUser(BaseModel):
    username: str
    email: str
    class Config:
        orm_mode = True

class ShowBlog(BaseModel):
    title: str
    content: str
    creator: Optional[ShowUser]  
    class Config:
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str