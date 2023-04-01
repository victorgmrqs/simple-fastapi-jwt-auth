from typing import Optional

from pydantic import BaseModel, HttpUrl


class Artigo(BaseModel):
    id: Optional[str] = None
    titulo: str
    descricao: str
    url_fonte: HttpUrl
    usuario_id: Optional[str]

    class Config:
        orm_mode = True
