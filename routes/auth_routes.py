from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["Autenticação"])

@auth_router.get("/")
async def index():
  # DocStrings:
  """
  Essa é a rota padrão de pedidos do sistema.
  """
  return {
    "Mensagem": "Rota padrão de autenticação", 
    "Autenticado": False
    }