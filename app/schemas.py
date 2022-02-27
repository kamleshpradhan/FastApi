from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime


# class Post(BaseModel):
#     title:str
#     content:str
#     published:bool
#     # published:bool = True to set the default value to true
#     ratings:Optional[int] = None
class PostBase(BaseModel):
    title:str
    content:str
    published:bool

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass


class PostResponse(PostBase):
    id:int
    created_at:datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email:EmailStr
    password:str

    class Config:
        orm_mode = True

class AccessToken(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]
    