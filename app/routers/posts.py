from re import search
from threading import currentThread
from .. import schemas
from typing import List, Optional
from fastapi import Depends,status,Response,HTTPException,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import models,schemas,oauth2





router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)


# response_model=List[schemas.PostResponse]
@router.get("/",response_model =List[schemas.PostOut])
def get_posts(db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str] = ""):
# fetching data using sqlalchmeny and orm
    # all_posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).limit(limit).offset(skip).all()
    # all_posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter = True).group_by(models.Post.id).all()
    # print(results)
    return results


    # Normal way to fetch all posts using postgres commands
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # return {"message":posts}



@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post:schemas.PostCreate,db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=post.title,content=post.content,published=post.published)
    new_post = models.Post(**post.dict(),owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    

    # Normal sql code to create a new post
    # cursor.execute("""INSERT into posts (title,content,published) VALUES(%s,%s,%s) returning *""",(post.title,post.content,post.published))
    # posts = cursor.fetchone()
    # conn.commit()
    # return{"message":posts}

# def getPost(id):
#     for j in posts:
#         if(j["id"]==id):
#             return(j)
            


# response_model=schemas.PostResponse
@router.get("/{id}",status_code = status.HTTP_200_OK,response_model=schemas.PostOut)
def get_post(id:int,response:Response,db:Session = Depends(get_db)):
    # post_id = getPost(id)

    # normal way to write in sql
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""" ,(str(id),))
    # post_id = cursor.fetchone()
    # conn.commit()

    # post_id = db.query(models.Post).filter(models.Post.id == id).first()
    post_id = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found.")
    #    response.status_code = status.HTTP_404_NOT_FOUND
    #    return {"message":f"No post with id {id} found"}

    return post_id

# def delPost(id):
#     for i,j in enumerate(posts):
#         if(j["id"]==id):
#             return i

@router.delete("/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session =Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    del_post = db.query(models.Post).filter(models.Post.id==id)

    # Normal sql code to delete a post
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(str(id),))
    # del_post = cursor.fetchone()
    # conn.commit()

    # ////Normal code to run the api in python
    # index = delPost(id)
    # if index == None:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} dose not exsist")
    # posts.pop(index)
    # return Response(status_code = status.HTTP_204_NO_CONTENT)
    if not del_post.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} dose not exsist")

    if del_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No Authorised to perform requested action")

    del_post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)



@router.put("/{id}",status_code = status.HTTP_202_ACCEPTED,response_model = schemas.PostResponse)
def update_post(id:int,updated_post:schemas.PostUpdate,db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    up_post = post_query.first()
    # Normal sql commands
    # cursor.execute("""UPDATE posts SET title=%s,content = %s,published = %s WHERE id = %s returning *""",(post.title,post.content,post.published,str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # index = delPost(id)
    # if index == None:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} dose not exsist")

    # post_dict = post.dict()
    # post_dict["id"] = id
    # posts[index] = post_dict
    if not up_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} dose not exsist")

    if up_post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return up_post;

