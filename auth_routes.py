from fastapi import APIRouter, Depends, HTTPException
from models import Usuario, Pedido
from dependecies import get_session
from main import bcrypt_context, ALG, ACESS_TOKEN_EXPIRE, SECRET_KEY
from schemas import UsuarioSchema,LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACESS_TOKEN_EXPIRE)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": id_usuario, "exp": data_expiracao}
    jwt_encode = jwt.encode(dic_info, SECRET_KEY, ALG)
    return jwt_encode

def verificar_token(token, session):
    usuario = session.query(Usuario).filter(Usuario.id==1).first()
    return usuario
    
def autenticacar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    else:
        return usuario

@auth_router.get("/")
async def auth():
    """
    Essa é a rota padrão de autenticação do sitema
    """
    return {"mensagem" : "Rota autenticação", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(get_session)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"Usuário cadastrado com sucesso {usuario_schema.email}"}
    
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    usuario = autenticacar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        acess_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "acess_token": acess_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
            }
    
@auth_router.get("/refresh")
async def use_refresh_token(token):
    usuario = verificar_token(token)
    acess_token = criar_token(usuario.id) 
    return {
            "acess_token": acess_token,
            "token_type": "Bearer"
            }  