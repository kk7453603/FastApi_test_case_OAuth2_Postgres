from sqlalchemy import Column, Integer, String

from postgres import Base

class User(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True)
    login = Column(String,nullable=False)
    first_name = Column(String,nullable=False)
    last_name = Column(String,nullable=False)
    passwd = Column(String)
    salt= Column(String)
    email = Column(String)
