from fastapi import Depends, HTTPException
from main import ALGORITHM, SECRET_KEY, oauth2_schema
from models.models import Usuario, db
from sqlalchemy.orm import Session, sessionmaker
from jose import jwt, JWTError

def pegar_sessao():
  try:
    Session = sessionmaker(bind=db)
    session = Session()
    yield session
  finally:
    session.close()

def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
  try:
    dicionario_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
    id_usuario = int(dicionario_info.get("sub"))
  except JWTError as error:
    print(error)
    raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token")
    
  usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
  if not usuario:
    raise HTTPException(status_code=401, detail="Acesso inválido")
  return usuario
