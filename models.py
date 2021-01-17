from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DATE
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    last_name = Column(String, index=True)
    type_user = Column(Integer, index=True)
    user_password = Column(String)


class Products(Base):
    __tablename__ = "products"

    ref = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(DATE, index=True)
    price = Column(Integer, index=True)
    qty = Column(Integer, index=True)
    category = Column(String, index=True)
    url = Column(String, index=True)
