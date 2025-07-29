from fastapi import APIRouter

order_router = APIRouter(prefix="/order", tags=["Pedidos"])

@order_router.get("/")
async def index():
  return {
    "Mensagem": "Você acessou a rota padrão de pedidos."
    }