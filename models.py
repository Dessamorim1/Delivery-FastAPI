from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base


db = create_engine("sqlite:///database/banco.db")

Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer)
    nome = Column("nome", String)
    email = Column("email", String)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean)