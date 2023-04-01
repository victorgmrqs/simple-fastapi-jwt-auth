from typing import List
from sqlalchemy import Integer, String, Column, Boolean

from sqlalchemy.orm import relationship

from core.config import settings


class Usuario(settings.DBBaseModel):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(256), nullable=True)
    sobrenome: str = Column(String(256), nullable=True)
    email: str = Column(String(256), nullable=False, unique=True)
    senha: str = Column(String(256), nullable=False)
    admin: str = Column(Boolean, default=False)
    artigos: List[str] = relationship(
        'Artigo',
        cascade='all,delete-orphan',
        back_populates='criador',
        uselist=True,
        lazy='joined',
    )
