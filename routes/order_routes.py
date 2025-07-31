from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from models import Pedido, Usuario
from schemas import OrderSchema

order_router = APIRouter(prefix="/order", tags=["Pedidos"], dependencies=[Depends(verificar_token)])

@order_router.get("/")
async def index():
  """
  Essa é a rota padrão de pedidos do nosso sistema. Todas as rotas dos pedidos precisam de autenticação
  """
  return {
    "Mensagem": "Você acessou a rota padrão de pedidos."
    }

@order_router.post("/pedido")
async def criar_pedido(order_schema: OrderSchema, session: Session = Depends(pegar_sessao)):
  novo_order = Pedido(usuario=order_schema.id_usuario)
  session.add(novo_order)
  session.commit()
  return {
    "mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_order.id}"
  }

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancela_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
  # usuario.admin = True
  # usuario.id = pedido.usuario
  pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
  if not pedido:
    raise HTTPException(status_code=400, detail="Pedido não encontrado")
  if not usuario.admin and usuario.id != pedido.usuario:
    raise HTTPException(status_code=401, detail="Você não tem autorização para realizar essa modificação.")

  pedido.status = "CANCELADO"
  session.commit()
  return {
    "mensagem": f"Pedido número: {pedido.id} cancelado com sucesso",
    "pedido": pedido
  }
