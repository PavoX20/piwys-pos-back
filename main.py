from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <--- 1. Importar esto
from app.core.database import engine, Base
from app.routers import auth, products, orders, payments

Base.metadata.create_all(bind=engine)

app = FastAPI(title="POS System")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
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