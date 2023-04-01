from pydantic import BaseModel
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from schemas.artigo import Artigo


class Usuario(BaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr
    admin: bool = False

    class Config:
        orm_mode = True


class UsuarioCreate(Usuario):
    senha: str


class UsuariosArtigos(Usuario):
    artigos: Optional[List[Artigo]]


class UsuarioUpdate(Usuario):
    nome: Optional[str]
    sobrenome: Optional[str]
    email: Optional[EmailStr]
    admin: Optional[bool]


class UsuarioUpdateSenha(UsuarioUpdate):
    senha: Optional[str]
