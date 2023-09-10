from pydantic import BaseModel, EmailStr

class Users(BaseModel):
    id:int
    strUserName: str
    strEmail: EmailStr
    class Config:
        from_attributes = True
