from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
from auth import criar_hash, verificar_senha, criar_token, usuario_logado
from tags import tags_metadata

app = FastAPI(title='API de Tarefas com Auth — Aula 6',
              description=""" ## API de gerenciamento de tarefas.""",
              version='1.0.0',
              openapi_tags=tags_metadata,
              )

# Banco em memória
tarefas  = []
usuarios = []
proximo_id_tarefa  = 1
proximo_id_usuario = 1

# Schemas 
class TarefaCreate(BaseModel):
    titulo:    str  = Field(..., min_length=2, max_length=200)
    descricao: str  = Field(..., max_length=500)

class TarefaPatch(BaseModel):
    titulo:    Optional[str]  = Field(None, min_length=2, max_length=200)
    descricao: Optional[str]  = Field(None, max_length=500)
    concluida: Optional[bool] = None

class UsuarioCreate(BaseModel):
    nome:  str = Field(..., min_length=2, max_length=100)
    email: str
    senha: str = Field(..., min_length=8)

class LoginRequest(BaseModel):
    email: str
    senha: str

class TokenResponse(BaseModel):
    access_token: str
    token_type:   str = 'bearer'

# Função auxiliar 
def achar_tarefa(tarefa_id: int):
    t = next((t for t in tarefas if t['id'] == tarefa_id), None)
    if not t:
        raise HTTPException(404, f'Tarefa {tarefa_id} não encontrada')
    return t

#  AUTENTICAÇÃO
# POST /usuarios - Cadastrar novo usuário
@app.post('/auth/registro', 
          tags=['Autenticação'],
          summary='Criação de conta',
          description='Cria uma nova conta com nome, e-mail e senha.',
          responses={
              201: {'description': 'Conta criada com sucesso'},
               409: {'description': 'E-mail ja cadastrado'},
               422: {'description': 'Dados inválidos'}})

def registro(dados: UsuarioCreate):
    global proximo_id_usuario
    if any(u['email'] == dados.email for u in usuarios):
        raise HTTPException(409, 'E-mail já cadastrado')
    novo = {
        'id':         proximo_id_usuario,
        'nome':       dados.nome,
        'email':      dados.email,
        'hash_senha': criar_hash(dados.senha),
    }
    usuarios.append(novo)
    proximo_id_usuario += 1
    return {'id': novo['id'], 'nome': novo['nome'], 'email': novo['email']}

@app.post('/auth/login', response_model=TokenResponse,
          tags=['Autenticação'],
          summary='Fazer login e obter token JWT.',
          description='Autentica o usuário e retorna um token JWT. Use o token no botão **Authorize**',
          responses={
               200: {'description': 'Login realizado - token retornado'},
               401: {'description': 'E-mail ou senha icorretos'},
          })
def login(dados: LoginRequest):
    usuario = next((u for u in usuarios if u['email'] == dados.email), None)
    if not usuario or not verificar_senha(dados.senha, usuario['hash_senha']):
        raise HTTPException(401, 'E-mail ou senha incorretos')
    token = criar_token({'sub': usuario['email'], 'nome': usuario['nome']})
    return {'access_token': token, 'token_type': 'bearer'}

# TAREFAS

# PÚBLICO - sem Depends
@app.get('/tarefas',
         tags=['Tarefas'],
          summary='Listar tarefas',
          description='Lista todas as tarefas.',
          responses={
              200: {'description': 'Lista retornada com sucesso.'},
          })
def listar():
    return tarefas

# PROTEGIDO - exige token
@app.post('/tarefas',
          tags=['Tarefas'],
          summary='Criação de tarefas',
          description='Criar uma nova tarefa.',
          responses={
              201: {'description': 'Tarefa criada com sucesso'},
          })
def criar(
    dados: TarefaCreate,
    email: str = Depends(usuario_logado)   # qualquer logado cria
):
    global proximo_id_tarefa
    nova = {
        'id':        proximo_id_tarefa,
        'titulo':    dados.titulo,
        'descricao': dados.descricao,
        'concluida': False,
    }
    tarefas.append(nova)
    proximo_id_tarefa += 1
    return nova

# PROTEGIDO
@app.patch('/tarefas/{tarefa_id}',
           tags=['Tarefas'],
          summary='Atualização de tarefas.',
          description='Atualiza titulo e descrição.',
          responses={
              200: {'description': 'Dados atualizados'},
          })
def atualizar(
    tarefa_id: int,
    dados: TarefaPatch,
    email: str = Depends(usuario_logado)
):
    t = achar_tarefa(tarefa_id)
    if dados.titulo    is not None: t['titulo']    = dados.titulo
    if dados.descricao is not None: t['descricao'] = dados.descricao
    if dados.concluida is not None: t['concluida'] = dados.concluida
    return t

# PROTEGIDO
@app.delete('/tarefas/{tarefa_id}',
            tags=[''],
          summary='Criação de conta',
          description='',
          responses={})
def remover(
    tarefa_id: int,
    email: str = Depends(usuario_logado)
):
    global tarefas
    achar_tarefa(tarefa_id)
    tarefas = [t for t in tarefas if t['id'] != tarefa_id]
    return {'mensagem': f'Tarefa {tarefa_id} removida'}