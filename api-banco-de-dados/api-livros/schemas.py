from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy.sql import func

# Entrada: POST e PUT (campos obrigatórios)
class LivroCreate(BaseModel):
    titulo: str = Field(..., min_length=2, max_length=100)
    autor: float = Field(..., gt=0) # gt=0 - maior que zero
    ano_publicação: int = Field(0, ge=0) # ge=0 - maior ou igual a zero
    disponivel: bool = Field()
    criado_em: datetime = Field(None, server_default=func.now())

# Entrada: PATCH (todos os campos são opcionais)
class LivroPatch(BaseModel):
    titulo: Optional[str] = Field(None, min_length=2, max_length=100)
    autor: Optional[float] = Field(None,  gt=0)
    ano_publicação: Optional[int] = Field(None,  gt=0)
    disponivel: Optional[bool] = Field(None, default=True)
    criado_em: Optional[datetime] = Field(None, server_default=func.now())

# Saída: (valor) que a API retorna
class LivroResponse(BaseModel):
    id: int
    titulo: str
    autor: float
    ano_publicação: int
    disponivel: bool
    criado_em: datetime

class Config:
    from_attributes = True # permite converter SQ