from lib2to3.pgen2.token import OP
from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException,Depends
from pydantic import BaseModel, BaseSettings
from . import models,schemas,utils
from sqlalchemy.orm import Session
from .database import engine,get_db
from .routers import posts,users,auth,vote
# from .config import settings


app = FastAPI()

models.Base.metadata.create_all(bind=engine)



# user = ["Raj","Shyam","Hari","Kishan"]
# posts = [
#     {
#     "id":1,
#     "title": "Intelligent Investor1",
#     "content": "A brief hstory about an Intelligent invester1",
#     "published":True,
#     "ratings":1},
#     {"id":2,
#     "title": "Intelligent Investor2",
#     "content": "A brief hstory about an Intelligent invester2",
#     "published":True,
#     "ratings":1},
#     {"id":3,
#     "title": "Intelligent Investor3",
#     "content": "A brief hstory about an Intelligent invester3",
#     "published":True,
#     "ratings":1},
#     {"id":4,
#     "title": "Intelligent Investor4",
#     "content": "A brief hstory about an Intelligent invester4",
#     "published":True,
#     "ratings":1
#     }
#     ]





# app.include_router(posts.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(vote.router)
@app.get("/")
def read_root():
    return{"message":"Hello World"}

# @app.get("/users")
# def get_users():
#     return{"users":user}

# def get_userby(id):
#     return(user[id-1])
# @app.get("/user/{id}")
# def get_user(id:int):
#     return {"user":get_userby(id)}



# All the routes are related to the posts.
# ----------------------------------------------------------------


# Demo route to test the
# @app.get("/test")
# def test(db:Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return{"status":posts}





# ----------------------------------------------------User Section-----------------------------
