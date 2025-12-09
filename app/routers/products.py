from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.models import models
from app.schemas import products as schemas
from app.core.deps import get_current_user # <--- 1. Importamos la dependencia

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    dependencies=[Depends(get_current_user)] # <--- 2. CANDADO MAESTRO: Todo lo de abajo requiere Token
)

# Ya no necesitamos pedir el usuario en cada función para validar, 
# el router lo hace por nosotros. Solo pedimos 'db'.

# --- OBTENER TODOS ---
@router.get("/", response_model=List[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).filter(models.Product.deleted_at == None).all()
    return products

# --- CREAR PRODUCTO ---
@router.post("/", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# --- EDITAR PRODUCTO ---
@router.put("/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, product_update: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id, models.Product.deleted_at == None).first()
    
    if not db_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if product_update.name is not None:
        db_product.name = product_update.name
    if product_update.description is not None:
        db_product.description = product_update.description
    if product_update.price is not None:
        db_product.price = product_update.price

    db.commit()
    db.refresh(db_product)
    return db_product

# --- ELIMINAR (SOFT DELETE) ---
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not db_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db_product.deleted_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Producto eliminado correctamente (Soft Delete)"}