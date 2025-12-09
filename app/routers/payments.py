from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models import models
from app.schemas import payments as schemas
from app.core.deps import get_current_user

router = APIRouter(
    prefix="/payments",
    tags=["Payment Methods"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=List[schemas.PaymentMethodResponse])
def get_payment_methods(db: Session = Depends(get_db)):
    return db.query(models.PaymentMethod).filter(models.PaymentMethod.is_active == True).all()