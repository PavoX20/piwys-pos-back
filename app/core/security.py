import bcrypt
from datetime import datetime, timedelta
from jose import jwt
import os

# Configuración JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 

# --- CAMBIO IMPORTANTE: Lógica con Bcrypt puro ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Bcrypt requiere bytes, así que convertimos las strings
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password_byte_enc = hashed_password.encode('utf-8')
    
    # checkpw compara la contraseña plana con el hash
    return bcrypt.checkpw(password_byte_enc, hashed_password_byte_enc)

def get_password_hash(password: str) -> str:
    # 1. Convertir password a bytes
    pwd_bytes = password.encode('utf-8')
    # 2. Generar salt y hashear
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    # 3. Devolver como string para guardar en la BD
    return hashed.decode('utf-8')

# --- FIN DEL CAMBIO ---

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt