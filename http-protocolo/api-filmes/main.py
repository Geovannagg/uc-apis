from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title='API de Filmes', version='1.0.0')

filmes = [
    {"id": 1, "nome": "Scooby-Doo: O Filme", "ano":2002, "diretor": "Raja Gosnell", "nota": 10},
    {"id": 2, "nome": "Como se fosse a primeira vez", "ano": 2004, "diretor": "Peter Sega", "nota": 10},
    {"id": 3, "nome": "Hellraiser: Renascido do Inferno", "ano": 1987, "diretor": "Clive Barker", "nota": 8.7}
]
proximo_id = 4

class FilmeCreate(BaseModel):
    titulo:  str
    diretor: str
    ano:     int
    nota:    float

@app.get('/filmes')
def listar_filmes():
    return filmes

@app.get('/filmes/{filme_id}')
def buscar_filme(filme_id: int):
    filme = next((f for f in filmes if f['id'] == filme_id), None)
    if not filme:
        return {'erro': f'Filme {filme_id} não encontrado'}
    return filme

@app.post('/filmes', status_code=201)
def criar_filme(filme: FilmeCreate):
    global proximo_id
    novo = {
        'id':      proximo_id,
        'nome':  filme.titulo,
        'diretor': filme.diretor,
        'ano':     filme.ano,
        'nota':    filme.nota,
    }
    filmes.append(novo)
    proximo_id += 1
    return novo