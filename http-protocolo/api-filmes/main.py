from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title= 'API de flimes', version='1.0.0')

filmes = [
    {"id": 1, "nome": "Scooby-Doo: O Filme", "ano":2002, "diretor": "Raja Gosnell", "nota": 0},
    {"id": 2, "nome": "Como se fosse a primeira vez", "ano": 2004, "diretor": "Peter Sega", "nota": 0},
   {"id": 3, "nome": "Hellraiser: Renascido do Inferno", "ano": 1987, "diretor": "Clive Barker", "nota": 0}
]
proximo_id = 4

class FilmeCreate(BaseModel):
    id: int
    nome: str
    ano: int
    diretor: str
    nota: float

@app.get('/filmes')
def listar_filmes():
    return filmes

@app.get('/filmes/{filme_id}')
def buscar_filme(filme_id: int):
    # Percorre a lista procurando o produto com aquele id
    filme = next(
        (f for f in filmes if f['id'] == filme_id),
        None  # valor padrão se não encontrar
    )
    if filme is None:
        return {'erro': f'Filme {filme_id} não encontrado'}
    return filme

@app.post('/filmes', status_code=201)
def criar_filme(filme: FilmeCreate):
    global proximo_id

novo_filme = {
    'id': proximo_id,
    'nome': filme.nome,
    'ano': filme.ano,
    'diretor': filme.diretor,
    'nota': filme.nota,
}
filmes.append(novo_filme)
proximo_id += 1

return novo_filme
