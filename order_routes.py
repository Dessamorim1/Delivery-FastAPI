from fastapi import APIRouter

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/")
async def home():
    """
    Essa é a rota padrão de pedidos do sitema. Todas as rotas dos pedidos precisam de autenticação.
    """
    return {"mensagem" : "Rota pedidos"}
