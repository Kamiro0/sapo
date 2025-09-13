from fastapi import Depends, HTTPException, status, APIRouter, Body
from sqlmodel import Session
from app.database import get_session
from app.schemas.schemas import EnvioCreate, EnvioOut, EnvioUpdate
from app.models.models import Envio as EnvioModel, EstadoEnum
from app.crud.crud_envio import create_envio, get_envio, list_envios, update_envio, delete_envio
from app.auth.auth import verify_token
from typing import List, Optional
from uuid import uuid4
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter(prefix="/envios", tags=["envios"])

def _gen_tracking():
    return "C-" + uuid4().hex[:10].upper()

def get_current_user(token: str = Depends(lambda: None)):
    # placeholder; real dependency injected in main() via Depends
    return None

@router.post("/", response_model=EnvioOut, status_code=201)
def crear_envio(envio: EnvioCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Token inválido")
    if user["role"] not in ("cliente","admin"):
        raise HTTPException(status_code=403, detail="No tienes permiso para crear envíos")
    env_model = EnvioModel(
        remitente=envio.remitente,
        destinatario=envio.destinatario,
        direccion_origen=envio.direccion_origen,
        direccion_destino=envio.direccion_destino,
        peso=envio.peso,
        descripcion=envio.descripcion,
        tracking_number=_gen_tracking(),
        estado=EstadoEnum.pendiente,
        creado_por=user["username"]
    )
    return create_envio(db, env_model)

@router.get("/", response_model=List[EnvioOut])
def listar_envios(
    estado: Optional[EstadoEnum]=None,
    creador: Optional[str]=None,
    limit:int=100,
    offset:int=0,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_session)
):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Token inválido")
    if user["role"] == "cliente":
        creador = user["username"]
    return list_envios(db, skip=offset, limit=limit, estado=estado, creador=creador)

@router.get("/{envio_id}", response_model=EnvioOut)
def obtener_envio(
    envio_id:int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_session)
):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Token inválido")
    envio = get_envio(db, envio_id)
    if not envio:
        raise HTTPException(status_code=404, detail="Envío no encontrado")
    if user["role"] in ("admin","repartidor") or envio.creado_por==user["username"]:
        return envio
    raise HTTPException(status_code=403, detail="Acceso prohibido")

@router.patch("/{envio_id}/estado", response_model=EnvioOut)
def actualizar_estado(
    envio_id:int,
    nuevo_estado: EstadoEnum = Body(..., embed=True),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_session)
):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Token inválido")
    if user["role"] not in ("repartidor","admin"):
        raise HTTPException(status_code=403, detail="Solo repartidor o admin puede actualizar estado")
    envio = get_envio(db, envio_id)
    if not envio:
        raise HTTPException(status_code=404, detail="Envío no encontrado")
    return update_envio(db, envio, {"estado": nuevo_estado})

@router.put("/{envio_id}", response_model=EnvioOut)
def actualizar_envio(
    envio_id:int,
    envio_update: EnvioUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_session)
):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Token inválido")
    envio = get_envio(db, envio_id)
    if not envio:
        raise HTTPException(status_code=404, detail="Envío no encontrado")
    if user["role"]=="admin" or envio.creado_por==user["username"]:
        return update_envio(db, envio, envio_update.dict(exclude_unset=True))
    raise HTTPException(status_code=403, detail="No tienes permisos para actualizar")

@router.delete("/{envio_id}", status_code=204)
def eliminar_envio(
    envio_id:int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_session)
):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Token inválido")
    if user["role"]!="admin":
        raise HTTPException(status_code=403, detail="Solo admin puede eliminar envíos")
    envio = get_envio(db, envio_id)
    if not envio:
        raise HTTPException(status_code=404, detail="Envío no encontrado")
    delete_envio(db, envio)
    return