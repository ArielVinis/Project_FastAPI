from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from models import Pedido
from schemas import OrderSchema

order_router = APIRouter(prefix="/order", tags=["Pedidos"])

@order_router.get("/")
async def index():
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