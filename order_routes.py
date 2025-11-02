from fastapi import APIRouter, Depends,HTTPException
from dependecies import get_session
from sqlalchemy.orm import Session
from schemas import PedidoSchema
from models import Pedido

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/")
async def home():
    """
    Essa é a rota padrão de pedidos do sitema. Todas as rotas dos pedidos precisam de autenticação.
    """
    return {"mensagem" : "Rota pedidos"}

@order_router.post("/criar_pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(get_session)):
    novo_pedido = Pedido(pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem" : f"pedido criado com sucesso ID do pedido: {novo_pedido.id}"}