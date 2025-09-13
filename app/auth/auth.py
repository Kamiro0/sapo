from datetime import datetime, timedelta
from jose import jwt

from app.core.config import settings

# Usuarios de prueba
USERS = {
    "cliente": {"username": "leon_cliente", "role": "cliente"},
    "repartidor": {"username": "repartidor", "role": "repartidor"},
    "admin": {"username": "admin", "role": "admin"},
}

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    from jose import JWTError, jwt
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None