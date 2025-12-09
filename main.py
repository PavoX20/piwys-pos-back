from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <--- 1. Importar esto
from app.core.database import engine, Base
from app.routers import auth, products, orders, payments
import os

app = FastAPI(title="POS System")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://piwys.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Permitir estos dominios
    allow_credentials=True,
    allow_methods=["*"],         # Permitir todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],         # Permitir todos los headers (Authorization, etc.)
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(payments.router)

@app.get("/")
def read_root():
    return {"message": "Sistema POS Estructurado y Listo 🚀"}

@app.get("/config-check")
def check_config():
    secret = os.getenv("SECRET_KEY")
    return {
        "API_STATUS": "OK",
        "SECRET_KEY_READ": "OK" if secret and len(secret) > 10 else "FAIL",
        "SECRET_KEY_TRUNCATED": secret[:5] if secret else "NOT_FOUND" # Mostramos los primeros 5 para verificar que no esté vacío
    }