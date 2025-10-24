from fastapi import APIRouter, Depends
from models import Usuario
from dependecies import get_session
from main import bcrypt_context

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def auth():
    """
    Essa é a rota padrão de autenticação do sitema
    """
    return {"mensagem" : "Rota autenticação", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(nome:str, email: str, senha: str, session = Depends(get_session)):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if usuario:
        return {"mensagem": "Já existe um usuário com esse email"}
    else:
        senha_criptografada = bcrypt_context.hash(senha)
        novo_usuario = Usuario(nome, email, senha_criptografada)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "Usuário cadastrado com sucesso"}

