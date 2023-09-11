from fastapi import FastAPI, Depends, status, HTTPException, APIRouter
from app.db import get_db
from typing import List, Optional
from sqlalchemy.orm import Session
from .. import models, schemas, response, utils



router = APIRouter(
    # prefix="/users"
    tags = ['Users']
)

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=response.Users)
async def signup_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.strPassword)
    user.strPassword = hashed_password
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.put("/users/{id}", response_model=response.Users)
def update_users(id:int, users: schemas.UserBase, db: Session = Depends(get_db)):
    user_query= db.query(models.Users).filter(models.Users.id == id)
    user = user_query.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    user_query.update(users.dict(), synchronize_session=False)
    db.commit()
    return user_query.first()


@router.get("/users", response_model=List[response.Users])
async def get_all_users(db: Session = Depends(get_db), limit:Optional[int]= None, search:Optional[ str]=None):
    users_query = db.query(models.Users)
    if search is not None and search != "None":
        users_query = users_query.filter(models.Users.strUserName.contains(search))
    if limit is not None:
        users_query = users_query.limit(limit)

    users = users_query.all()
    return users

@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_users(id:int, db: Session = Depends(get_db)):
    user= db.query(models.Users).filter(models.Users.id == id)
    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    
    user.delete(synchronize_session=False)
    db.commit()


@router.get("/users/{id}", response_model=List[response.Users])
async def get_product( id:int, db: Session = Depends(get_db)):
    user_query = db.query(models.Product).filter(models.Users.id == id).first()
    if not user_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} was not found")
    return {user_query}