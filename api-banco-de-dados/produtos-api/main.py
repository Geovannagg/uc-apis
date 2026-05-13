from fastapi import FastAPI
from database import engine, Base
from router import router as produto_router

Base.metadata.create.all(bind=engine)

app = FastAPI(
    title= "API de Produtos da Gê",
    description="CRUD com Fastapi, SQLAlchemy,SQlite",
    version="2.0.0"

)

app.include_router(produto_router)

@app.get('/')
def raiz():
    return {"status": "online", "docs": "/docs", "versao": "2.0.0"}