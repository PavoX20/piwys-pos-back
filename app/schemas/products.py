from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base para compartir atributos comunes
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

# Lo que recibimos al CREAR un producto
class ProductCreate(ProductBase):
    pass

# Lo que recibimos al ACTUALIZAR (todo opcional)
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

# Lo que devolvemos al frontend (leída)
class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    # No devolvemos deleted_at porque el front solo verá los activos
    
    class Config:
        from_attributes = True