from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    email: str
    password: str

class User(UserBase):
    id: int
    login: str
    first_name: str
    last_name: str
    email : str
    
    class Config:
        orm_mode = True

class UserStatus(UserBase):
    status:str


class UserGetInfo(UserBase):
    first_name: str
    last_name: str