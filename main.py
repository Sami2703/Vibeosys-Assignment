from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from database import Product, SessionLocal
from schemas import ProductCreate, ProductUpdate, Product
from typing import List

#Initialize FastAPI app
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. List all products with pagination
@app.get("/product/list", response_model=List[Product])
def list_products(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

# 2. View information about a specific product
@app.get("/product/{pid}/info", response_model=Product)
def get_product(pid: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == pid).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# 3. Add a new product
@app.post("/product/add", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(
        name=product.name,
        category=product.category,
        description=product.description,
        productimage_url=product.productimage_url,
        sku=product.sku,
        unit_of_measure=product.unit_of_measure,
        lead_time=product.lead_time
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# 4. Update an existing product
@app.put("/product/{pid}/update", response_model=Product)
def update_product(pid: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == pid).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.name = product.name
    db_product.category = product.category
    db_product.description = product.description
    db_product.productimage_url = product.productimage_url
    db_product.sku = product.sku
    db_product.unit_of_measure = product.unit_of_measure
    db_product.lead_time = product.lead_time

    db.commit()
    db.refresh(db_product)
    return db_product
