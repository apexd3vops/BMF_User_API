from fastapi import FastAPI, Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session 
from .. import db, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])


@router.post("/auth")
def authenticate_user( user_credentials:schemas.UserAuth, db: Session = Depends(db.get_db)):
    user = db.query(models.Users).filter(models.Users.strEmail == user_credentials.strEmail).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.strPassword, user.strPassword):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id": user.strEmail, "user_id": user.id})
    return {"login":"successful","access_token": access_token, "token": "bearer"}