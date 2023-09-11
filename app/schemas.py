from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    strUserName: str
    strPassword: str
    strEmail: EmailStr

class UserAuth(BaseModel):
    strEmail: EmailStr
    strPassword: str

