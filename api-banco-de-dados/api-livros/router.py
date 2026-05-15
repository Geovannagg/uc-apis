from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Livro
from schemas import LivroCreate, LivroPatch, LivroResponse

# APIRouter: agrupa os endpoints que registramos no main.py
router = APIRouter(prefix='/livros', tags=['Livros'])

# GET/produtos: Lista todos os Produtos
@router.get('/', response_model=List[LivroResponse])
def listar_livro(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Livro).filter(Livro.disponivel == True).offset(skip).limit(limit).all()

# GET/produtos/{id}: Busca um produto pelo id
@router.get('/{livro_id}', response_model=LivroResponse)
def buscar_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro or not livro.disponivel:
        raise HTTPException(status_code=404, detail=f'Livro {livro_id} não encontrado')
    return livro

# POST/produtos: Cria um produto
@router.post('/', response_model=LivroResponse, status_code=201)
def criar_livro(dados: LivroCreate, db: Session = Depends(get_db)):
    livro = Livro(
        titulo = dados.titulo,
        autor = dados.autor,
        ano_publicação = dados.ano_publicação,
        disponivel = dados.disponivel,
        criado_em = dados.criado_em,
    )
    db.add(livro) # enfileirar o insert (produtos que vamos adicionar)
    db.commit() # executa no banco
    db.refresh(livro) # atualiza o objeto com id e criado_em do banco
    return livro

# PUT/produtos/{id}: Substitui o produto inteiro
@router.put('/{livro_id}', response_model=LivroResponse)
def substituir_livro(livro_id: int, dados: LivroCreate, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro or not livro.ativo:
        raise HTTPException(status_code=404, detail='Livro não encontrado')
    livro.titulo= dados.titulo
    livro.autor = dados.autor
    livro.ano_publicação = dados.ano_publicacao
    livro.disponivel = dados.disponivel
    livro.criado_em = dados.criado_em
    db.commit()
    db.refresh(livro)
    return livro

# PATCH/produtos/{id}: Atualiza só os campos enviados
@router.patch('/{livro_id}', response_model=LivroResponse)
def atualizar_livro(livro_id: int, dados: LivroPatch,
                      db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro or not livro.ativo:
        raise HTTPException(status_code=404, detail='Livro não encontrado')
    if dados.titulo is not None: livro.autor = dados.titulo
    if dados.autor is not None: livro.autor = dados.autor
    if dados.ano_publicacao is not None: livro.ano_publicacao = dados.ano_publicacao
    if dados.disponivel is not None: livro.disponivel = dados.disponivel
    if dados.criado_em is not None: livro.criado_em = dados.criado_em
    db.commit()
    db.refresh(livro)
    return livro

# DELETE/produtos/{id}: marca ativo = False
@router.delete('/{livro_id}')
def remover_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro or not livro.disponivel:
        raise HTTPException(status_code=404, detail='Livro não encontrado')
    livro.disponivel = False
    db.commit()
    return {'mensagem': f'Livro {livro_id} removido'}
