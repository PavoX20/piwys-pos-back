from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

# Importaciones internas
from app.core.database import get_db
from app.models import models
from app.schemas import auth as schemas
from app.core import security

router = APIRouter(tags=["Authentication"])

# --- ENDPOINT: REGISTRAR USUARIO ---
@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Verificar si el email o username ya existen
    user_exists = db.query(models.User).filter(
        (models.User.email == user.email) | (models.User.username == user.username)
    ).first()
    
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario o correo ya están registrados"
        )

    # 2. Hashear la contraseña
    hashed_password = security.get_password_hash(user.password)

    # 3. Guardar en BD
    new_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# --- ENDPOINT: LOGIN ---
@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm espera recibir 'username' y 'password' desde el form-data
    
    # 1. Buscar usuario
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    # 2. Verificar usuario y contraseña
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Generar JWT
    access_token = security.create_access_token(data={"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}