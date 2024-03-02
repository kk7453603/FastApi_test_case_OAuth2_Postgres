from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    login: str
    first_name: str
    last_name: str
    email : str
    
    class Config:
        orm_mode = True