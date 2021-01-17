from datetime import date
from os import name
from typing import List, Optional

from pydantic import BaseModel


class ProductsBase(BaseModel):
    ref: int
    name: str
    date: date
    price: int
    qty: int
    category: str


class ProductsCreate(ProductsBase):
    pass


class Products(ProductsBase):
    
    ref: int
    name: str
    date: date
    price: int
    qty: int
    category: str

    class Config:
        orm_mode = True

class ProductsQTY(BaseModel):
    qty: int

class UserBase(BaseModel):
    username: str
    email: str
    name: str
    last_name: str
    type_user: int

class UserIn(BaseModel):
    username    : str
    password    : str


class UserCreate(UserBase):
    password: str

class User(UserBase):
    username: str
    email: str
    name: str
    last_name: str
    type_user: int
    user_password: str

    class Config:
        orm_mode = True

class UserRecover(BaseModel):
    user_password: str
