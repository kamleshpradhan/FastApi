from urllib import response
from app import schemas
# from .database import client,session
import pytest
from jose import JWSError, jwt
from app.config import settings


# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == "Hello World"
#     assert res.status_code == 200

def test_create_user(client):
    # to send the data in the body/
    res = client.post("/users/",json={"email":"abcde@gmail.com","password":"password123"})
    # print(res.json())
    new_user = schemas.UserOut(**res.json())
    assert new_user.email=="abcde@gmail.com"
    assert res.status_code == 201

def test_login_user(client,test_user):
    res = client.post("/login",data={"username":test_user["email"],"password":test_user["password"]})
    login_token = schemas.AccessToken(**res.json())
    # print(login_token)
    payload = jwt.decode(login_token.access_token, settings.secret_key, algorithms=[settings.algorithim])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_token.token_type == "bearer_token"
    # print(res.json())
    assert res.status_code == 200

# @pytest.mark.parametrize("email","password","status_code",[()])
# add all the data to test with different scenarios
def test_incorrect_login(client,test_user):
    res = client.post("/login",data ={"username":test_user["email"],"password":"password"})
    # print(res.json())
    assert res.status_code == 403
    assert res.json().get('detail') == "Invalid Credentials" 

