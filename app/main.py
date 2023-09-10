from typing import List, Optional
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, status, HTTPException
from . import models, schemas, response
from app.db import setting, engine, get_db



app = FastAPI()

models.Base.metadata.create_all(bind=engine)

while True:
    try: 
        conn = psycopg2.connect(host= f'{setting.DATABASE_HOSTNAME}', database = f'{setting.DATABASE_NAME}', user=f'{setting.DATABASE_USERNAME}', password= f'{setting.DATABASE_PASSWORD}', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Succesfull Database Handshake")
        break
    except Exception as error:
        print("Database Handshake Failed")
        print("Error: ", error)
        time.sleep(10)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/signup", status_code=status.HTTP_201_CREATED, response_model=response.Users)
async def signup_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/oauth")
def login_user():
    return {"User": "Successfully logged in"}


@app.put("/users/{id}", response_model=response.Users)
def update_users(id:int, users: schemas.UserBase, db: Session = Depends(get_db)):
    user_query= db.query(models.Users).filter(models.Users.id == id)
    user = user_query.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    user_query.update(users.dict(), synchronize_session=False)
    db.commit()
    return user_query.first()


@app.get("/users", response_model=List[response.Users])
async def get_all_users(db: Session = Depends(get_db), limit:Optional[int]= None, search:Optional[ str]=None):
    users_query = db.query(models.Users)
    if search is not None and search != "None":
        users_query = users_query.filter(models.Users.strUserName.contains(search))
    if limit is not None:
        users_query = users_query.limit(limit)

    users = users_query.all()
    return users

@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_users(id:int, db: Session = Depends(get_db)):
    user= db.query(models.Users).filter(models.Users.id == id)
    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    
    user.delete(synchronize_session=False)
    db.commit()


@app.get("/users/{id}", response_model=List[response.Users])
async def get_product( id:int, db: Session = Depends(get_db)):
    user_query = db.query(models.Product).filter(models.Users.id == id).first()
    if not user_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} was not found")
    return {user_query}
  