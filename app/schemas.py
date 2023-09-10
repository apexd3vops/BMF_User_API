from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    strUserName: str
    strPassword: str
    strEmail: EmailStr
