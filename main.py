from typing import List

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost.tiangolo.com", "https://localhost.tiangolo.com",
    "http://localhost", "http://localhost:8080", "http://localhost:8081","http://localhost:8082", "https://inventoryonclick.herokuapp.com"
]
app.add_middleware(
    CORSMiddleware, allow_origins=origins,
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

# Dependency
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

########################
@app.post("/login/")
async def auth_user(userAuth: schemas.UserIn, db: Session = Depends(get_db)):
    user_in_db = crud.get_user_by_username(db, username=userAuth.username)
    if user_in_db is None:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    
    if check_password_hash(user_in_db.user_password, userAuth.password) is False:
        raise HTTPException(status_code=403, detail="Error de autenticacion")

    return  {"Autenticado": True,  "Tipo": user_in_db.type_user}
##############

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username no disponible")
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_user}", response_model=schemas.User)
async def read_user(user_user: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_username=user_user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user


@app.post("/products/", response_model=schemas.Products)
async def create_product(
    product: schemas.ProductsCreate, db: Session = Depends(get_db)
):
    return crud.create_product(db=db, product=product)

@app.get("/products/", response_model=List[schemas.Products])
async def read_products(db: Session = Depends(get_db)):
    products = crud.get_products(db)
    return products

@app.get("/products/{ref}", response_model=schemas.Products)
async def read_products_by_ref(ref:int, db: Session = Depends(get_db)):
    products = crud.get_product_id(db, ref=ref)
    if products is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    return products

@app.get("/products/{ref}/qty")
async def read_qty_by_ref(ref:int, db: Session = Depends(get_db)):
    products = crud.get_product_id(db, ref=ref)
    if products is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    products.qty
    return products.qty

@app.put("/products/{ref}", response_model=schemas.Products)
async def update_qty(ref: int, product: schemas.ProductsQTY, db: Session = Depends(get_db)):
    product_in = crud.get_product_id(db, ref)
    product_in.qty=product.qty
    db.commit()
    return product_in

@app.put("/products/", response_model=schemas.Products)
async def update_product(ref: int, product: schemas.ProductsUpdate, db: Session = Depends(get_db)):
    product_in = crud.get_product_id(db, ref)
    product_in.name=product.name
    product_in.date=product.date
    product_in.price=product.price
    product_in.qty=product.qty
    product_in.category=product.category
    db.commit()
    return product_in

@app.put("/users/")
async def recover_pass(password: str, user: schemas.UserRecover, db: Session = Depends(get_db)): 
    recover = crud.get_user_by_key(db, password=password)
    recover.user_password = generate_password_hash(user.user_password)
    db.commit()
    return {"Pass_Recovered": True}

@app.delete("/products/{ref}")
async def delete_products(ref: int, db: Session = Depends(get_db)): 
    products = crud.get_product_id(db, ref)
    if products is None:
        raise HTTPException(status_code=404, detail="El producto no existe")
    db.delete(products)
    db.commit()
    return {"Delete successfull": True}


@app.get("/recovery/")
async def get_email(mail: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=mail)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    else:
        msg = MIMEMultipart()
        message = ("Recupere su cuenta accediendo al siguiente enlace: \n \n https://inventoryonclick.herokuapp.com/recuperar/"+db_user.user_password +"\n \n")
        password = "Inventory-Onclick123"
        msg['From'] = "inventory.onclick@gmail.com"
        msg['To'] = db_user.email
        msg['Subject'] = "Recuperacion de Credenciales Inventory Onclick"
        msg.attach(MIMEText(message, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login(msg['From'], password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()

    return db_user.user_password

