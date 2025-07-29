from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base

# cria a conexão do seu banco
db = create_engine ("sql:///banco.db")

# cria a base do seu banco de dados
Base = declarative_base()

# criar as classes/tabelas do seu banco
# Usuario

class Usuario(Base):
  __tablename__ = "usuarios"

  id = Column("id", Integer, primary_key=True, autoincrement=True)
  nome = Column("nome", String)
  email = Column("email", String, nullable=False)
  senha = Column("senha", String)
  ativo = Column("ativo", Boolean)
  admin = Column("admin", Boolean, default=False)

  def __init__(self, nome, email, senha, ativo=True, admin=False):
    self.nome = nome
    self.email = email
    self.senha = senha
    self.ativo = ativo
    self.admin = admin

# Pedidos
class Pedido(Base):
  __tablename__ = "pedidos"

  id = Column("id", Integer, primary_key=True, autoincrement=True)
  status = Column("status", String) #pendente, em preparacao, cancelado, finalizado
  usuario = Column("usuario", ForeignKey("usuarios.id"))
  preco = Column("preco", Float)
  #itens = 

  def __init__(self, usuario, status="PENDENTE", preco=0):
    self.usuario = usuario
    self.status = status
    self.preco = preco

# ItensPedidos


# executa a criação dos metadados do seu banco (cria efetivamente o banco de dados)
