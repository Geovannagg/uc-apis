from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="API de Tarefas",
    version="1.0.0"
)

tarefas = [
    {"id": 1, "titulo": "Pintar", "descricao": "Pintar quadros decorativos para casas", "concluida": False},
    {"id": 2, "titulo": "Dar aula", "descricao": "Levar os aluno ao museu de arte romana", "concluida": False},
    {"id": 3, "titulo": "Estudar", "descricao": "Revisar conteúdos importantes", "concluida": False},
]
proximo_id = 4

class TarefaCreate(BaseModel):
    titulo: str
    descricao: str
    concluida: bool = False

class TarefaPatch(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    concluida: Optional[bool] = None

def encontrar_tarefa(tarefa_id: int):
    tarefa = next((t for t in tarefas if t["id"] == tarefa_id), None)
    if tarefa is None: 
        raise HTTPException(
        status_code = 404, 
        detail = f"Tarefa com id {tarefa_id} não encontrada."
        )
    return tarefa

@app.get('/tarefas')
def listar_tarefas():
    return tarefas

@app.get('/tarefas/{tarefa_id}')
def buscar_tarefa(tarefa_id: int):
    return encontrar_tarefa(tarefa_id)

@app.post('/tarefas', status_code=201)
def criar_tarefa(tarefa: TarefaCreate):
    global proximo_id
    nova = {
        'id': proximo_id,
        'titulo': tarefa.titulo,
        'descricao': tarefa.descricao,
        'concluida': tarefa.concluida,
    }
    tarefas.append(nova)
    proximo_id += 1
    return nova

@app.put('/tarefas/{tarefa_id}')
def substituir(tarefa_id: int, dados: TarefaCreate):
    tarefa = encontrar_tarefa(tarefa_id)
    tarefa['titulo'] = dados.titulo
    tarefa['descricao'] = dados.descricao
    tarefa['concluida'] = dados.concluida
    return tarefa

@app.patch('/tarefas/{tarefa_id}')
def atualizar(tarefa_id: int, dados: TarefaPatch):
    tarefa = encontrar_tarefa(tarefa_id)
    if dados.titulo is not None: tarefa = tarefa['titulo'] = dados.titulo
    if dados.descricao is not None: tarefa = tarefa['descricao'] = dados.descricao
    if dados.concluida is not None: tarefa = tarefa['concluida'] = dados.concluida
    return tarefa

@app.delete('/tarefas/{tarefa_id}')
def remover(tarefa_id: int):
    global tarefas 
    encontrar_tarefa(tarefa_id)
    tarefas = [t for t in tarefas if t ['id'] != tarefa_id]
    return {'mensagem': f'Tarefas {tarefa_id} removida com sucesso!'}
