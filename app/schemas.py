from pydantic import BaseModel,EmailStr, conint
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



class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
        orm_mode = True
class PostResponse(PostBase):
    id:int
    created_at:datetime
    content:str
    title:str
    published:bool
    owner_id:int
    owner:UserOut

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
    

class Vote(BaseModel):
    post_id:int
    dir: conint(le=1)


class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True
