from typing import Dict
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import models, schemas

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_key(db: Session, password: str):
    return db.query(models.User).filter(models.User.user_password == password).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_product_id(db: Session, ref: int):
    return db.query(models.Products).filter(models.Products.ref == ref).first()

def get_user(db: Session, user_username: str):
    return db.query(models.User).filter(models.User.username == user_username).first()

def create_user(db: Session, user: schemas.UserCreate):
    n_password = generate_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, name=user.name, last_name=user.last_name, type_user=user.type_user, user_password=n_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    msg = MIMEMultipart()
    message = ("Bienvenido a Inventory Onclick su Cuenta ha sido creada satisfactoriamente y sus credenciales son: \n \n Usuario:" 
        + user.username + "\n Contraseña:" + user.password + "\n \n")
    password = "Inventory-Onclick123"
    msg['From'] = "inventory.onclick@gmail.com"
    msg['To'] = user.email
    msg['Subject'] = "Bienvenido a Inventory Onclick"
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()

    return db_user

def get_products(db: Session):
    return db.query(models.Products).offset(0).limit(1000).all()

def create_product(db: Session, product: schemas.ProductsCreate):
    db_product = models.Products(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product

