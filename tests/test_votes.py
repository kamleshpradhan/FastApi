from pytest import fixture
from app import models


import pytest
from app import models

@pytest.fixture()
def test_vote(test_post,session,test_user):
    test_vote = models.Vote(post_id=test_post[3].id,user_id=test_user["id"])
    session.add(test_vote)
    session.commit()


def test_votes(authorized_client,test_post,test_user2):
   res = authorized_client.post("/vote/",json={"post_id":test_post[3].id,"dir": 1})
   assert res.status_code == 201


def test_votes_twice(authorized_client,test_post,test_vote):
    print(test_post[3])
    res = authorized_client.post("/vote/",json={"post_id":test_post[3].id,"dir":1})
    assert res.status_code == 409
    # assert res.status_code == 201

def test_delete_a_vote(authorized_client,test_post,test_vote):
    res = authorized_client.post("/vote/",json={"post_id":test_post[3].id,"dir":0})
    assert res.status_code == 201

def test_delete_vote_non_exsist(authorized_client,test_post,test_vote):
     res = authorized_client.post("/vote/",json={"post_id":test_post[3].id,"dir":0})
     assert res.status_code == 404
    

def test_delete_vote_non_exsist(authorized_client,test_post,test_vote):
     res = authorized_client.post("/vote/",json={"post_id":80000,"dir":1})
     assert res.status_code == 404

def test_vote_on_unauthorized_user(client,test_post,test_vote):
     res = client.post("/vote/",json={"post_id":test_post[3].id,"dir":1})
    #  print(res.json())
     assert res.status_code == 401