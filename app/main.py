from datetime import timedelta
import re
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models,crud,schemas,crypt

from postgres import SessionLocal,engine

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



models.Base.metadata.create_all(bind=engine)



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/sign-up", response_model=schemas.UserStatus)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    db_user = crud.get_user_by_email(db, email=user.email)
    if (re.fullmatch(regex, user.email)==None):
        raise HTTPException(status_code=409, detail="Invalid Email Address")
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    newUser=crud.create_user(db=db, user=user)
    return {"email":newUser.email,"status":"ok"}


@app.get("/users/", response_model=List[schemas.UserGetInfo])
def read_users(db: Session = Depends(get_db)):
    users = crud.get_all_users(db)
    return users



@app.post("/login", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=form_data.username)
    if db_user==None or not (crypt.verify_hash(form_data.password,db_user.salt).decode('utf-8') == db_user.passwd):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    crud.update_user_status(db,db_user,True) 
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crypt.create_access_token(data={"sub": db_user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token}



@app.get("/user/me/", response_model=schemas.UserGetInfo)
async def get_current_user(token: schemas.Token,db: Session = Depends(get_db)):    
    if len(token.access_token)!=32:
        raise HTTPException(status_code=401,detail="Incorrect JWT token",headers={"WWW-Authenticate": "Bearer"})
    email=crypt.get_current_user_email(token.access_token)
    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return db_user

@app.post("/user/me/",response_model=schemas.UserStatus)
async def change_current_user(new_first_name:str,new_last_name:str,token: schemas.Token,db: Session = Depends(get_db)):
    if len(token.access_token)!=32:
        raise HTTPException(status_code=401,detail="Incorrect JWT token",headers={"WWW-Authenticate": "Bearer"})
    email=crypt.get_current_user_email(token.access_token)
    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=401, detail="User not found")
    result=crud.update_user(db,email,new_first_name,new_last_name)
    return {"email":result.email,"status":"ok"}


@app.post("/refresh", response_model=schemas.Token)
async def refresh_token(token: schemas.Token, db: Session = Depends(get_db)):
    if len(token.access_token)!=32:
        raise HTTPException(status_code=401,detail="Incorrect JWT token",headers={"WWW-Authenticate": "Bearer"})
    email = crypt.get_current_user_email(token.access_token)
    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = crypt.create_access_token(data={"sub": db_user.email}, expires_delta=access_token_expires)
    return {"access_token": new_access_token}


@app.get("/logout",response_model=schemas.UserStatus)
async def logout(token: schemas.Token,db: Session = Depends(get_db)):
    if len(token.access_token)!=32:
        raise HTTPException(status_code=401,detail="Incorrect JWT token",headers={"WWW-Authenticate": "Bearer"})
    email = crypt.get_current_user_email(token.access_token)
    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=401, detail="User not found")
    crud.update_user_status(db,db_user,False)
    return {"email":db_user.email,"status":"ok"}