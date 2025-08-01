from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from models import ItemPedido, Pedido, Usuario
from schemas import ItemPedidoSchema, OrderSchema, ResponsePedidoSchema
from typing import List

order_router = APIRouter(prefix="/order", tags=["Pedidos"], dependencies=[Depends(verificar_token)])

@order_router.get("/")
async def home():
  """
  Essa é a rota padrão de pedidos do nosso sistema. Todas as rotas dos pedidos precisam de autenticação
  """
  return {
    "Mensagem": "Você acessou a rota padrão de pedidos."
    }

@order_router.post("/pedido")
async def criar_pedido(order_schema: OrderSchema, session: Session = Depends(pegar_sessao)):
  novo_order = Pedido(usuario=order_schema.usuario)
  session.add(novo_order)
  session.commit()
  return {
    "mensagem": "Pedido criado com sucesso.",
    "ID do pedido": f"{novo_order.id}"
  }

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
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

@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
  """
    Apenas Admins podem ver todos os pedidos do sistema.
  """
  if not usuario.admin:
    raise HTTPException(status_code=401, detail="Você não tem autorização para realizar essa ação")
  else:
    todos_pedidos = session.query(Pedido).all()
    return {
      "pedidos": todos_pedidos
    }

@order_router.post("/pedido/adicionar_item/{id_pedido}")
async def adicionar_item_pedido(
    id_pedido: int, 
    item_pedido_schema: ItemPedidoSchema, 
    session: Session = Depends(pegar_sessao), 
    usuario: Usuario = Depends(verificar_token)
  ):
  pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
  if not pedido:
    raise HTTPException(status_code=400, detail="Pedido não encontrado")
  if not usuario.admin and usuario.id != pedido.usuario:
    raise HTTPException(status_code=401, detail="Você não tem autorização para realizar essa ação")
  item_pedido = ItemPedido(
    item_pedido_schema.quantidade,
    item_pedido_schema.sabor,
    item_pedido_schema.tamanho,
    item_pedido_schema.preco_unitario,
    id_pedido
  )

  session.add(item_pedido)
  pedido.calcular_preco()
  session.commit()
  return {
    "mensagem": "Item adicionado ao pedido com sucesso.",
    "item_id": item_pedido.id,
    "preco_pedido": pedido.preco
  }

@order_router.post("/pedido/remover_item/{id_item_pedido}")
async def remover_item_pedido(
    id_item_pedido: int, 
    session: Session = Depends(pegar_sessao), 
    usuario: Usuario = Depends(verificar_token)
  ):
  item_pedido = session.query(ItemPedido).filter(ItemPedido.id==id_item_pedido).first()
  pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido).first()

  if not item_pedido:
    raise HTTPException(status_code=400, detail="Item no pedido não encontrado")
  if not usuario.admin and usuario.id != pedido.usuario:
    raise HTTPException(status_code=401, detail="Você não tem autorização para realizar essa ação")

  session.delete(item_pedido)
  pedido.calcular_preco()
  session.commit()
  return {
    "mensagem": "Item removido do pedido com sucesso.",
    "preco_pedido": pedido.preco,
    "pedido": pedido
  }

# finalziar um pedido
@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
  pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
  if not pedido:
    raise HTTPException(status_code=400, detail="Pedido não encontrado")
  if not usuario.admin and usuario.id != pedido.usuario:
    raise HTTPException(status_code=401, detail="Você não tem autorização para realizar essa modificação.")

  pedido.status = "FINALIZADO"
  session.commit()
  return {
    "mensagem": f"Pedido número: {pedido.itens} finalizado com sucesso",
    "pedido": pedido
  }

# visualizar 1 pedido
@order_router.get("/pedido/{id_pedido}")
async def visualizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
  pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
  if not pedido:
    raise HTTPException(status_code=400, detail="Pedido não encontrado")
  if not usuario.admin and usuario.id != pedido.usuario:
    raise HTTPException(status_code=401, detail="Você não tem autorização para realizar essa modificação.")
  return {
    "quantidade_itens_pedido": len(pedido.itens),
    "pedido": pedido
  }

# visualizar todos os pedidos de 1 usuário
@order_router.get("/listar/pedidos_usuario", response_model=List[ResponsePedidoSchema])
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedidos_usuario = session.query(Pedido).filter(Pedido.usuario==usuario.id).all()
    return pedidos_usuario
