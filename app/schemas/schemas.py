from pydantic import BaseModel, Field
from typing import Optional
from app.models.models import EstadoEnum

class EnvioCreate(BaseModel):
    remitente: str
    destinatario: str
    direccion_origen: str
    direccion_destino: str
    peso: float = Field(..., gt=0)
    descripcion: Optional[str] = None

class EnvioUpdate(BaseModel):
    remitente: Optional[str] = None
    destinatario: Optional[str] = None
    direccion_origen: Optional[str] = None
    direccion_destino: Optional[str] = None
    peso: Optional[float] = Field(None, gt=0)
    descripcion: Optional[str] = None
    estado: Optional[EstadoEnum] = None

class EnvioOut(BaseModel):
    id: int
    remitente: str
    destinatario: str
    direccion_origen: str
    direccion_destino: str
    peso: float
    descripcion: Optional[str]
    tracking_number: str
    estado: EstadoEnum
    creado_por: str
    
    class Config:
       from_attributes = True