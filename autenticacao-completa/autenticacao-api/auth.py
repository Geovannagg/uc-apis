import bcrypt 
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "senai-taguatinga-chave-2026"
ALGORITHM = 'HS256'
EXPIRA_MIN = 60

#httpbearer: faz o swagger mostrar o campo simples para colar o token
security = HTTPBearer 

def criar_hash(senha: str) -> str:
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

def verificar_senha(senha: str, hash_salvo: str) -> bool:
    return bcrypt.checkpw(senha.encode(), hash_salvo.encode())

def criar_token(dados: dict) -> str:
    payload = dados.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes= EXPIRA_MIN)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def usuario_logado(
        credendials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),) -> str:
    token = credendials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(401, "Token Inválido!")
        return email
    except JWTError:
        raise HTTPException(401, "Token inválido ou expirado.")