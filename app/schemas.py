from pydantic import BaseModel

class UserBase(BaseModel):
    strUserName: str
    strPassword: str
