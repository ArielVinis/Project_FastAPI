from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Usuario
from dependencies import pegar_sessao, verificar_token
from main import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, bcrypt_context, ALGORITHM
from schemas import LoginSchema, UsuarioSchema
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["Autenticação"])

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
  data_expiracao = datetime.now(timezone.utc) + duracao_token
  dicionario_info = {
    "sub": str(id_usuario), 
    "exp": data_expiracao
    }
  jwt_codificado = jwt.encode(dicionario_info, SECRET_KEY, ALGORITHM)
  return jwt_codificado

def autenticar_usuario(email, senha, session):
  usuario = session.query(Usuario).filter(Usuario.email==email).first()
  if not usuario:
    return False
  elif not bcrypt_context.verify(senha, usuario.senha):
    return False
  return usuario


@auth_router.get("/")
async def home():
  # DocStrings:
  """
  Essa é a rota padrão de autenticação do sistema.
  """
  return {
    "Mensagem": "Você acessou a rota padrão de autenticação", 
    "Autenticado": False
    }

@auth_router.post("/criar_conta")
async def criar_conta(
  usuario_schema: UsuarioSchema, 
  session = Depends(pegar_sessao),
  ):

  usuario_existente = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
  if usuario_existente:
    raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado")
  
  else:
    senha_ciptografada = bcrypt_context.hash(usuario_schema.senha)
    novo_usuario = Usuario(
      usuario_schema.nome, 
      usuario_schema.email, 
      senha_ciptografada, 
      usuario_schema.ativo, 
      usuario_schema.admin
      )
    session.add(novo_usuario)
    session.commit()
    return {
      "mensagem:": f"usuário cadastrado com sucesso: {usuario_schema.email}"
    }

@auth_router.post("/login")
async def login(login_chema: LoginSchema, session: Session = Depends(pegar_sessao)):
  usuario = autenticar_usuario(login_chema.email, login_chema.senha, session)
  if not usuario:
    raise HTTPException(status_code=400, detail="Usuário não encontrado ou senha incorreta.")
  else:
    access_token = criar_token(usuario.id)
    refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
    return {
      "access_token": access_token,
      "refresh_token": refresh_token,
      "token_type": "Bearer"
      }

@auth_router.post("/login_form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
  """
    Essa parte é apenas para acessar o "Available authorizations".
    \nAssim, você consegue acessar as rotas que requerem estar autorizados e sem precisar realizar requisições de teste a todo instante para as rotas.
  """
  usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
  if not usuario:
    raise HTTPException(status_code=400, detail="Usuário não encontrado ou senha incorreta.")
  else:
    access_token = criar_token(usuario.id)
    return {
      "access_token": access_token,
      "token_type": "Bearer"
      }

@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
  access_token = criar_token(usuario.id)
  return {
      "access_token": access_token,
      "token_type": "Bearer"
      }
