from sqlmodel import Session, select
from app.models.models import Envio, EstadoEnum
from typing import List, Optional

def create_envio(db: Session, envio: Envio) -> Envio:
    db.add(envio)
    db.commit()
    db.refresh(envio)
    return envio

def get_envio(db: Session, envio_id: int) -> Optional[Envio]:
    statement = select(Envio).where(Envio.id == envio_id)
    res = db.exec(statement).first()
    return res

def list_envios(db: Session, skip: int = 0, limit: int = 100, estado: Optional[EstadoEnum]=None, creador: Optional[str]=None) -> List[Envio]:
    statement = select(Envio)
    if estado:
        statement = statement.where(Envio.estado == estado)
    if creador:
        statement = statement.where(Envio.creado_por == creador)
    statement = statement.offset(skip).limit(limit)
    return db.exec(statement).all()

def update_envio(db: Session, envio: Envio, data: dict) -> Envio:
    for key, value in data.items():
        setattr(envio, key, value)
    db.add(envio)
    db.commit()
    db.refresh(envio)
    return envio

def delete_envio(db: Session, envio: Envio):
    db.delete(envio)
    db.commit()
