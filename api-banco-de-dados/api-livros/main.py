from fastapi import FastAPI
from database import engine, Base
from router import router as livro_router

#Cria as tabelas no banco ao iniciar a API, se o banco.db não existir, ele cria o arquivo e as tabelas, se já existir, ele não faz nada - não apaga os dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Livro",
    description="CRUD com FastAPI + SQLAlchemy + SQlite",
    version="1.0.0"
)

#Registra o router com prefixo /produtos
app.include_router(livro_router)

@app.get('/')
def raiz():
    return{"status": "online", "docs": "/docs", "versao": "1.0.0"}
