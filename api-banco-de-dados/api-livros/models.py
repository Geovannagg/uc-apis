from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base # importa a base que criamos no database.py
class Livro(Base):
    __tablename__ = 'livros' # nome da tabela no banco

# colunas da tabela
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    autor = Column(String(100), nullable=False)
    ano_publicacao = Column(Integer, default=0)
    disponivel = Column(Boolean, default=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

# __repr__: como o objeto aparece no terminal
    def __repr__(self):
       return f'<Livro id={self.id} titulo={self.titulo}>'
