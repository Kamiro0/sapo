from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum

class EstadoEnum(str, Enum):
    pendiente = 'pendiente'
    en_transito = 'en_transito'
    entregado = 'entregado'
    cancelado = 'cancelado'

class Envio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    remitente: str
    destinatario: str
    direccion_origen: str
    direccion_destino: str
    peso: float
    descripcion: Optional[str] = None
    tracking_number: str
    estado: EstadoEnum
    creado_por: str
