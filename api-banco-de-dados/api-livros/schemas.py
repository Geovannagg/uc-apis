from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Entrada: POST e PUT (campos obrigatórios)
class LivroCreate(BaseModel):
    titulo: str = Field(..., min_length=2, max_length=100)
    autor: str = Field(..., min_length=2, max_length=100) 
    ano_publicacao: int = None


# Entrada: PATCH (todos os campos são opcionais)
class LivroPatch(BaseModel):
    titulo: Optional[str] = Field(None, min_length=2, max_length=100)
    autor: Optional[str] = Field(None,  min_length=2, max_length=100)
    ano_publicacao: Optional[int] = None
    disponivel: Optional[bool] = None

# Saída: (valor) que a API retorna
class LivroResponse(BaseModel):
    id: int
    titulo: str
    autor: str
    ano_publicacao: int
    disponivel: bool
    criado_em: datetime

class Config:
    from_attributes = True # permite converter SQ