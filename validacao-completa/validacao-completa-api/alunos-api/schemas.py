from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
from typing import Optional
from datetime import datetime

# Schema de CRIAÇÃO (POST)
# Contém senha pois o usuário precisa enviar para se cadastrar.
# NÃO contém id nem criado_em / o banco gera automaticamente.
class AlunoCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100, description='Nome completo do aluno')
    email: EmailStr = Field(..., max_length=8, description='Exatamente 8 caracteres') # Usando EmailStr importado
    matricula: str = Field(..., min_length=8, description='Mínimo 8 caracteres')
    nota_final: float = Field(ge=0, le=10)

    @field_validator('nome')
    @classmethod
    def nome_sem_numeros(cls, v: str) -> str:
        if any(char.isdigit() for char in v):
            raise ValueError('Nome não deve conter números!')
        if not v.strip():
            raise ValueError('Nome não pode ser só espaços!')
        return v.strip() #remove espaços extras das bordas
    
    @field_validator('matricula')
    @classmethod
    def matricula_deve_ter_numero(cls,v: str) -> str:
        tem_numero = any(c.isdigit() for c in v )
        if not tem_numero:
            raise ValueError('Matricula deve ter apenas números!')
        return v
    
class AlunoPatch(BaseModel):
    nota_final: Optional[float] = Field(None)
    email: Optional[EmailStr] = None

    @field_validator('nome')
    @classmethod
    def nome_sem_numeros(cls, v):
        if v is not None:
            v_clean = v.strip()
            if any(char.isdigit() for char in v_clean):
                raise ValueError('Nome não pode conter números!')
            if not v_clean:
                raise ValueError('Nome não pode ser só espaços!')
            return v_clean
        return v

class AlunoResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    ativo: bool
    matricula: str
    nota_final: float
    criado_em: datetime

    # Atualizado para o padrão Pydantic V2 (dentro da classe correspondente)
    model_config = ConfigDict(from_attributes=True) # converte SQLAlchemy → Pydantic
