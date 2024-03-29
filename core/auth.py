from pytz import timezone
from os import path
from typing import Optional, List

from datetime import datetime, timedelta


from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import EmailStr
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.usuario import Usuario as UsuarioModel

from core.config import settings
from core.security import verificar_senha


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=path.join(settings.API_V1_STR, 'usuarios', 'login')
)


async def autenticar(
    email: EmailStr, password: str, db: AsyncSession
) -> Optional[UsuarioModel]:
    # Sugestão do intelicode
    # async with AsyncSession as session:
    #     usuario = await session.execute(select(UsuarioModel).where(UsuarioModel.email == email))
    #     usuario = usuario.scalars().first()
    #     if usuario is None:
    #         return None
    #     if not await verificar_senha(password, usuario.senha):
    #         return None
    #     return usuario

    async with db as session:
        query = select(UsuarioModel).where(UsuarioModel.email == email)
        result = await session.execute(query)
        if usuario := result.scalars().unique().one_or_none():
            return None if not await verificar_senha(password, usuario.senha) else usuario
        else:
            return None


def _criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    sp: timezone = timezone('America/Sao_Paulo')
    expira: datetime = datetime.now(tz=sp) + tempo_vida

    payload: dict = {
        'type': tipo_token,
        'exp': expira,
        'iat': datetime.now(tz=sp),
        'sub': sub,
    }
    return jwt.encode(
        payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM
    )


def criar_token_acesso(sub: str) -> str:
    """https://jwt.io"""
    return _criar_token(
        tipo_token='access_token',
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )
