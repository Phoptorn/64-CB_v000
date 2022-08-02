from typing import List
from urllib import response
from fastapi import APIRouter, FastAPI ,HTTPException
from pydantic import BaseModel
from .database import conn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome back to FastAPI"}

# users = {"results":[{"gender":"male","name":{"title":"Mr","first":"Eirik","last":"Thon"},"location":{"street":{"number":744,"name":"Ole Reistads vei"},"city":"Trondheim","state":"Finnmark - Finnmárku","country":"Norway","postcode":"6518","coordinates":{"latitude":"45.0407","longitude":"-94.8304"},"timezone":{"offset":"+8:00","description":"Beijing, Perth, Singapore, Hong Kong"}},"email":"eirik.thon@example.com","login":{"uuid":"3dd1ad35-79c4-4d5d-a981-efe38e5b9d7d","username":"orangebutterfly897","password":"marble","salt":"CMVt2u2O","md5":"9487c3e310487d95325448d0d986b532","sha1":"3f6e12617d4ece272a5b150d49865c2dd8e860f0","sha256":"2fbcbbb25a611c3691d2dc829ce16fce00bc748cae14190a66e42ec5c93fe165"},"dob":{"date":"1999-05-17T00:37:35.318Z","age":23},"registered":{"date":"2020-07-12T00:23:13.578Z","age":2},"phone":"69376848","cell":"45991785","id":{"name":"FN","value":"17059948334"},"picture":{"large":"https://randomuser.me/api/portraits/men/20.jpg","medium":"https://randomuser.me/api/portraits/med/men/20.jpg","thumbnail":"https://randomuser.me/api/portraits/thumb/men/20.jpg"},"nat":"NO"}],"info":{"seed":"b78c86de1af99c50","results":1,"page":1,"version":"1.4"}}
# @app.get("/users")
# async def read_users():
#     return {"results":[{"gender":"male","name":{"title":"Mr","first":"Eirik","last":"Thon"},"location":{"street":{"number":744,"name":"Ole Reistads vei"},"city":"Trondheim","state":"Finnmark - Finnmárku","country":"Norway","postcode":"6518","coordinates":{"latitude":"45.0407","longitude":"-94.8304"},"timezone":{"offset":"+8:00","description":"Beijing, Perth, Singapore, Hong Kong"}},"email":"eirik.thon@example.com","login":{"uuid":"3dd1ad35-79c4-4d5d-a981-efe38e5b9d7d","username":"orangebutterfly897","password":"marble","salt":"CMVt2u2O","md5":"9487c3e310487d95325448d0d986b532","sha1":"3f6e12617d4ece272a5b150d49865c2dd8e860f0","sha256":"2fbcbbb25a611c3691d2dc829ce16fce00bc748cae14190a66e42ec5c93fe165"},"dob":{"date":"1999-05-17T00:37:35.318Z","age":23},"registered":{"date":"2020-07-12T00:23:13.578Z","age":2},"phone":"69376848","cell":"45991785","id":{"name":"FN","value":"17059948334"},"picture":{"large":"https://randomuser.me/api/portraits/men/20.jpg","medium":"https://randomuser.me/api/portraits/med/men/20.jpg","thumbnail":"https://randomuser.me/api/portraits/thumb/men/20.jpg"},"nat":"NO"}],"info":{"seed":"b78c86de1af99c50","results":1,"page":1,"version":"1.4"}}

#Data from mongo
class users(BaseModel):
    # username: str
    firstname: str
    lastname: str
    # password: str

class login_req(BaseModel):
    username: str
    # firstname: str
    # lastname: str
    password: str

@app.get("/FakeDB", response_model=List[users])
async def usersDB():
    msg_list = conn.fakeDB.fruit.find()
    response_msg_list = []
    for msg in msg_list:
        response_msg_list.append(users(**msg))
    return response_msg_list

#add_get_method (Find)
@app.get("/FakeDB_Find", response_model=users)
async def user_find(username: str, password: str):
    # username = "user1"
    user = conn.fakeDB.fruit.find_one(
        { "username": username }
    )
    if (user) is not None:
        user["id"] = str(user["_id"])
        if username == user["username"] and password == user["password"]:
            return user
        raise HTTPException(status_code=404, detail="Password ไม่ถูกต้อง")   
    else:
        raise HTTPException(status_code=404, detail="Not Found")


@app.post("/FakeDB", response_model=users)
async def create_users(users: users):
    conn.fakeDB.fruit.insert_one(users.dict())
    return users

#add_post
@app.post("/FakeDB_Login", response_model=users)
async def login(input: login_req):  
    user = conn.fakeDB.fruit.find_one({"username": input.username})
    if not user:
        raise HTTPException(status_code=404, detail="ไม่พบ")
    elif not (
        input.username == user["username"]
        and input.password == user["password"]
    ):
        raise HTTPException(status_code=404, detail="รหัสไม่ถูกต้อง")
    else:
        user["id"] = str(user["_id"])
    return user


@app.put("/FakeDB/{username}", response_model=users)
async def update_users(username: str, users: users):
    conn.fakeDB.fruit.update_one({"username": username}, {"$set": users.dict()})
    return users

@app.delete("/FakeDB/{username}", response_model=users)
async def delete_users(username: str):
    conn.fakeDB.fruit.delete_one({"username": username})
    return users(username=username)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



















