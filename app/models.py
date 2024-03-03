from sqlalchemy import Column, Integer, String, Boolean

from app.postgres import Base

class User(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True,nullable=False)
    email = Column(String,unique=True,nullable=False)
    first_name = Column(String,nullable=True)
    last_name = Column(String,nullable=True)
    passwd = Column(String)
    salt= Column(String)
    is_active = Column(Boolean, default=False)
