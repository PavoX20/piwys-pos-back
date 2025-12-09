from pydantic import BaseModel, EmailStr
from typing import Optional

# 1. Esquema para crear un usuario (Lo que envía el Front al registrarse)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# 2. Esquema para devolver datos de usuario (¡Sin la contraseña!)
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True # Esto permite leer datos directamente del modelo SQL

# 3. Esquema para el Token (Lo que devolvemos al hacer Login)
class Token(BaseModel):
    access_token: str
    token_type: str