from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.payments import PaymentMethodResponse # Importamos


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float
    class Config:
        from_attributes = True

# --- CAMBIO IMPORTANTE ---
class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    payment_method_id: int  # <--- AHORA ES OBLIGATORIO

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    created_at: datetime
    payment_method: Optional[PaymentMethodResponse] = None
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True