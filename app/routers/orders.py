from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import models
from app.schemas import orders as schemas
from app.core.deps import get_current_user
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session, joinedload

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=schemas.OrderResponse)
def create_order(
    order_data: schemas.OrderCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if not order_data.items:
        raise HTTPException(status_code=400, detail="El pedido no puede estar vacío")

    # 1. Validar Método de Pago
    payment_method = db.query(models.PaymentMethod).filter(models.PaymentMethod.id == order_data.payment_method_id).first()
    if not payment_method:
        raise HTTPException(status_code=404, detail="Método de pago no válido")

    total_order_amount = 0.0
    new_order_items = []

    # 2. Procesar Items
    for item in order_data.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if not product or product.deleted_at:
             raise HTTPException(status_code=400, detail=f"Producto {item.product_id} no disponible")

        price = float(product.price)
        subtotal = price * item.quantity
        total_order_amount += subtotal

        new_order_items.append(models.OrderItem(
            product_id=product.id,
            quantity=item.quantity,
            unit_price=price,
            subtotal=subtotal
        ))

    # 3. Crear Orden
    new_order = models.Order(
        user_id=current_user.id,
        payment_method_id=payment_method.id, # <--- GUARDAMOS EL PAGO
        total_amount=total_order_amount
    )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in new_order_items:
        item.order_id = new_order.id
        db.add(item)
    
    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("/", response_model=List[schemas.OrderResponse])
def read_orders(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # --- CAMBIO AQUÍ: Usamos options(joinedload(...)) ---
    # Esto le dice a la BD: "Trae la orden Y ADEMÁS trae los datos del método de pago de una vez"
    query = db.query(models.Order).options(joinedload(models.Order.payment_method))

    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.filter(models.Order.created_at >= start)
    
    if end_date:
        end = datetime.strptime(end_date, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
        query = query.filter(models.Order.created_at <= end)

    query = query.order_by(models.Order.created_at.desc())
    orders = query.offset(skip).limit(limit).all()
    
    return orders