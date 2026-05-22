from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
from typing import Optional
from datetime import datetime

# Schema de CRIAÇÃO (POST)
class AlunoCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100, description='Nome completo do aluno')
    # Ajustado: E-mails costumam ser maiores. Se a regra de 8 caracteres era para a matrícula, mude para lá!
    email: EmailStr = Field(..., description='E-mail válido do aluno') 
    matricula: str = Field(..., min_length=8, max_length=8, description='Exatamente 8 caracteres')
    nota_final: float = Field(0.0, ge=0, le=10)

    @field_validator('nome')
    @classmethod
    def nome_sem_numeros(cls, v: str) -> str:
        if any(char.isdigit() for char in v):
            raise ValueError('Nome não deve conter números!')
        if not v.strip():
            raise ValueError('Nome não pode ser só espaços!')
        return v.strip()
    
    @field_validator('matricula')
    @classmethod
    def matricula_deve_ter_numero(cls, v: str) -> str:
        tem_numero = any(c.isdigit() for c in v)
        if not tem_numero:
            raise ValueError('Matricula deve ter apenas números!')
        return v
    
# Schema de ATUALIZAÇÃO (PATCH)
class AlunoPatch(BaseModel):
    # ADICIONADO: O campo 'nome' precisava existir aqui para o validador funcionar!
    nota_final: Optional[float] = Field(None, ge=0, le=10)
    email: Optional[EmailStr] = None

class ErroResponse(BaseModel):
    detail: str

class AlunoResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    ativo: bool
    matricula: str
    nota_final: float
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)