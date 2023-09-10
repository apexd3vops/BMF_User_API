from pydantic import BaseModel

class Users(BaseModel):
    id:int
    strUserName: str
    strPassword: str
    class Config:
        from_attributes = True
