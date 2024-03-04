from pydantic import BaseModel


class Token(BaseModel):
    access_token: str


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
    is_active: bool

    class Config:
        orm_mode = True

class UserStatus(UserBase):
    status:str


class UserGetInfo(UserBase):
    first_name: str
    last_name: str