from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, session
from models import Usuario
from dependencies import pegar_sessao
from main import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, bcrypt_context, ALGORITHM
from schemas import LoginSchema, UsuarioSchema
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone


auth_router = APIRouter(prefix="/auth", tags=["Autenticação"])
duracao_token = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

def criar_token(id_usuario, duracao_token):
  data_expiracao = datetime.now(timezone.utc) + duracao_token
  dicionario_info = {
    "sub": id_usuario, 
    "exp": data_expiracao
    }
  jwt_codificado = jwt.encode(dicionario_info, SECRET_KEY, ALGORITHM)
  return jwt_codificado

def verificar_token(token, session=Depends(pegar_sessao)):
  # Verificar token
  # extrair o ID do usuário do token
  usuario = session.query(Usuario).filter(Usuario.id==1).first()
  return usuario

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
  Essa é a rota padrão de pedidos do sistema.
  """
  return {
    "Mensagem": "Você acessou a rota padrão de autenticação", 
    "Autenticado": False
    }

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session=Depends(pegar_sessao)):
  usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
  if usuario:
    # Já existe usuario com este email
    raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado")
  else:
    senha_ciptografada = bcrypt_context.hash(usuario_schema.senha)
    novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_ciptografada, usuario_schema.ativo, usuario_schema.admin)
    session.add(novo_usuario)
    session.commit()
    return {
      "mensagem:": f"usuário cadastrado com sucesso: {usuario_schema.email}"
    }

# login -> email e senha -> token JWT
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

@auth_router.get("/refresh")
async def use_refresh_token(token):
  usuario = verificar_token(token)
  access_token = criar_token(usuario.id)
  return {
      "access_token": access_token,
      "token_type": "Bearer"
      }
