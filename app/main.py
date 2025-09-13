from fastapi import FastAPI, Depends, HTTPException, status, Form, Security
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.routers import envio as envio_router
from app.database import init_db, get_session
from app.core.config import settings
from app.auth.auth import create_access_token, USERS
from datetime import timedelta
from typing import Dict

app = FastAPI(title=settings.PROJECT_NAME)  # <-- Primero crea la app

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Ahora sí, incluye los routers
app.include_router(envio_router.router)

@app.on_event('startup')
def on_startup():
    init_db()

@app.post('/token')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = USERS.get(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail='Usuario/credenciales inválidas')
    access_token = create_access_token({'username': user['username'], 'role': user['role']}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {'access_token': access_token, 'token_type': 'bearer'}

def get_raw_token(token: str = Depends(oauth2_scheme)):
    return token

from app.routers import envio as envio_mod
envio_mod.get_current_user = get_raw_token