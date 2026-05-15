from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#URL do banco - sqlite salva em um arquivvo banco.db na pasta do projeto 
DATABASE_URL = 'sqlite:///./banco.db'

# Engine: motor de conexão com o banco
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})

# SessionLocal: fãbrica de sessões - cada requisição tem sua sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: classe base que todos os modelos vão herdar
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db # yield: ecerra a sessão
    finally:
        db.close()