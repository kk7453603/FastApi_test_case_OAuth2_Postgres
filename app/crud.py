import base64
from sqlalchemy.orm import Session
import models, schemas
from os import urandom
from hashlib import pbkdf2_hmac



def get_user(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_all_users(db: Session):
    return db.query(models.User).all()

def create_user(db: Session, user: schemas.UserCreate):
    salt = urandom(32)
    key = pbkdf2_hmac('sha256',user.password.encode('utf-8'),salt=salt,iterations=100000)
    encsalt=base64.b64encode(salt)
    enckey=base64.b64encode(key)

    db_user = models.User(email=user.email,first_name="-",last_name="-",passwd=enckey.decode('utf-8'),salt=encsalt.decode('utf-8'))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, compare_email:str, new_first_name: str, new_last_name: str):
    currentUser = db.query(models.User).filter(models.User.email==compare_email).first()
    currentUser.first_name = new_first_name
    currentUser.last_name = new_last_name
    db.commit()
    db.refresh(currentUser)
    return currentUser

def update_user_status(db: Session,user:models.User,status:bool):
    user.is_active = status
    db.commit()
    db.refresh(user)
    return user

