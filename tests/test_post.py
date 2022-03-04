from typing import List
from app import schemas
import pytest
# def test_get_all_posts(authorized_client,test_post):
#     res = authorized_client.get("/posts/")
#     # posts = schemas.PostOut(res.json())
#     # print(res.json())//
#     def validate(post):
#         return schemas.PostOut(**post)
#     posts_map = map(validate,res.json())
#     posts_list = list(posts_map)
#     print(posts_list)
#     assert len(res.json()) == len(test_post)
#     assert res.status_code == 200
#     # assert posts_list[0].Post.id == test_post[0].id

# def test_unauthorized_user_get_all_posts(client,test_post):
#     res = client.get("/posts/")
#     assert res.status_code == 401


# def test_unauthorized_user_get_one_post(client,test_post):
#     res = client.get(f"/posts/{test_post[0].id}")
#     print(res.json())
#     assert res.status_code == 401

# def test_get_one_post_not_exist(authorized_client,test_post):
#     res = authorized_client.get(f"/posts/8888")
#     assert res.status_code == 404

# def test_get_one_post(authorized_client,test_post):
#     res = authorized_client.get(f"/posts/{test_post[0].id}")
#     print(res.json())
#     post = schemas.PostOut(**res.json())
#     assert post.Post.id == test_post[0].id
#     assert post.Post.content == test_post[0].content


# @pytest.mark.parametrize("title,content,published",[
#     ("title1","this is post 1",False),
#     ("title2","this is post 2",False),
#     ("title3","this is post 3",False),
#     ("title4","this is post 4",False),
#     ("title5","this is post 5",False)
# ])
# def test_create_post(authorized_client,test_user,test_post,title,content,published):
#     res = authorized_client.post("/posts/",json={'title':title,'content':content,'published':published})

#     created_post = schemas.Post(**res.json())
#     print(created_post)
#     assert res.status_code == 201
#     assert created_post.title == title 
#     assert created_post.content == content
#     assert created_post.published == published
#     assert created_post.owner_id == test_user['id'] 


# def test_create_post_default_published(authorized_client,test_user,test_post):
#     res = authorized_client.post("/posts/",json={'title':"title",'content':"content"})

#     created_post = schemas.Post(**res.json())
#     print(created_post)
#     assert res.status_code == 201
#     assert created_post.title == "title" 
#     assert created_post.content == "content"
#     assert created_post.published == True
#     assert created_post.owner_id == test_user['id'] 

# def test_unauthorized_user_create_post(client,test_user,test_post):
#     res = client.post("/posts/",json={'title':"title",'content':"content"})
#     print(res)
#     assert res.status_code == 401

# def test_unauthorized_user_delete_post(client,test_user,test_post):
#     res = client.delete(f"/posts/{test_post[0].id}")
#     assert res.status_code == 401




# def test_authorized_user_delete_post(authorized_client,test_user,test_post):
#     res = authorized_client.delete(f"/posts/{test_post[0].id}")
#     assert res.status_code == 204


# def test_delete_post_non_exsist(authorized_client,test_user,test_post):
#     res = authorized_client.delete(f"/posts/800000")
#     assert res.status_code == 404

# def test_delete_other_user_post(authorized_client,test_user,test_post):
#     res = authorized_client.delete(f"/posts/{test_post[4].id}")
#     assert res.status_code == 403

def test_delete_other_user_post(authorized_client,test_user,test_post):
    data = {
        "title":"updated title",
        "content":"updated content",
        "id":test_post[0].id
    }
    res = authorized_client.put(f"/posts/{test_post[0].id}",json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 202
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_other_user_post(authorized_client,test_user,test_user2,test_post):
    data = {
        "title":"updated title",
        "content":"updated content",
        "id":test_post[4].id
    }
    res = authorized_client.put(f"/posts/{test_post[4].id}",json=data)  
    assert res.status_code == 403

def test_unauthorized_user_update_post(client,test_user,test_post):
    res = client.put(f"/posts/{test_post[0].id}")
    assert res.status_code == 401

def test_update_post_non_exsist(authorized_client,test_user,test_post):
    data = {
        "title":"updated title",
        "content":"updated content",
        "id":test_post[3].id
    }
    res = authorized_client.put(f"/posts/800000",json=data)
    assert res.status_code == 404