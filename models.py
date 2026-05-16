from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    phone = Column(String, unique=True)
    hashed_password = Column(String)
