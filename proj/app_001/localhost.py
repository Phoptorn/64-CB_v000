from typing import List
from urllib import response
from fastapi import APIRouter, FastAPI ,HTTPException
from pydantic import BaseModel
from .database import conn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Data from local
class Item(BaseModel):
    name: str
    lastname: str
    email: str
    password: str
    age: int

fakeDatabase = {
    1: {"name": "John", "lastname": "Doe", "email": "john@email.com", "password": "name"+"123", "age": 30},
    2: {"name": "Jane", "lastname": "Doe",  "email": "jane@email.com", "password": "name"+"123", "age": 28},
    3: {"name": "Jack", "lastname": "Doe",  "email": "jack@email.com", "password": "name"+"123", "age": 25},
    4: {"name": "Jill", "lastname": "Doe",  "email": "jill@email.com", "password": "name"+"123", "age": 27},
    5: {"name": "Joke", "lastname": "Doe",  "email": "joke@email.com", "password": "name"+"123", "age": 26}
}

@app.get("/fakeDatabase/")
async def All_fakeDB():
    return fakeDatabase

@app.get("/fakeDatabase/{id}")
async def readItem(id: int):
    return fakeDatabase[id]

@app.post("/fakeDatabase/")
def addItem(name: str, lastname: str, email: str, password: str, age: int):
    newId = len(fakeDatabase.keys()) + 1
    fakeDatabase[newId] = {"name": name, "lastname": lastname, "email": email, "password": password, "age": age}
    return fakeDatabase[newId]

@app.put("/fakeDatabase/{id}")
def updateItem(id: int, item: Item):
    fakeDatabase[id]['name'] = item.name
    return fakeDatabase

@app.delete("/fakeDatabase/{id}")
def deleteItem(id: int):
    del fakeDatabase[id]
    return fakeDatabase

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)