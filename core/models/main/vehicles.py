from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Vehicle(BaseModel):
    id: Optional[int] = None
    plate: str = Field(..., max_length=7, description="Placa do veículo")
    brand: str = Field(..., max_length=100, description="Marca do veículo")
    model: str = Field(..., max_length=100, description="Modelo do veículo")
    year: int = Field(..., gt=1900, lt=2025, description="Ano do veículo")
    color: str = Field(..., max_length=50, description="Cor do veículo")
    user_id: Optional[int] = Field(None, description="ID do usuário associado ao veículo")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Data de criação do registro")

    class Config:
        orm_mode = True