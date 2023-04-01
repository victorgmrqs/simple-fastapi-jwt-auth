from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.config import settings


class Artigo(settings.DBBaseModel):
    __tablename__ = 'artigos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(256))
    descricao: str = Column(String(256))
    url_fonte: str = Column(String(256))
    usuario_id: int = Column(Integer, ForeignKey('usuarios.id'))
    criador = relationship('Usuario', back_populates='artigos', lazy='joined')
