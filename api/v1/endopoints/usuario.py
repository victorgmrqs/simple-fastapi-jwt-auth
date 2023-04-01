from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import autenticar, criar_token_acesso
from core.common import get_session, get_current_user
from core.security import gerar_hash_senha

from models.usuario import Usuario as UsuarioModel
from schemas.usuario import Usuario as UsuarioSchema
from schemas.usuario import (
    UsuarioCreate,
    UsuariosArtigos,
    UsuarioUpdate,
    UsuarioUpdateSenha,
)


router = APIRouter()


@router.get('/logado', response_model=UsuarioSchema)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    return usuario_logado


@router.post(
    '/signup',
    status_code=status.HTTP_201_CREATED,
    response_model=UsuarioSchema,
)
async def post_usuario(
    usuario: UsuarioCreate, session: AsyncSession = Depends(get_session)
):
    novo_usuario: UsuarioModel = UsuarioModel(
        senha=gerar_hash_senha(usuario.senha), **usuario.dict()
    )

    async with session:
        try:
            session.add(novo_usuario)
            await session.commit()
            return novo_usuario
        # TODO: Arrumar o erro de veriricação se o usuário já existe
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail='Usuário já cadastrado',
            )


@router.get(
    '/', status_code=status.HTTP_200_OK, response_model=List[UsuarioSchema]
)
async def get_usuarios(session: AsyncSession = Depends(get_session)):
    async with session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioModel] = result.scalars().unique().all()

    return usuarios


@router.get(
    '/{usuario_id}',
    status_code=status.HTTP_200_OK,
    response_model=UsuariosArtigos,
)
async def get_usuario(
    usuario_id: int,
    session: AsyncSession = Depends(get_session),
):
    async with session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioModel = result.scalars().unique().one_or_none()

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Usuario não encontrado',
            )
        return usuario


@router.patch(
    '/{usuario_id}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=UsuarioSchema,
)
async def patch_usuario(
    usuario_id: int,
    usuario: UsuarioUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user),
):
    async with session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_up: UsuarioModel = result.scalars().unique().one_or_none()

        if not usuario_up:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Usuario não encontrado',
            )

        if usuario.nome:
            usuario_up.nome = usuario.nome

        if usuario.sobrenome:
            usuario_up.sobrenome = usuario.sobrenome
        if usuario.email:
            usuario_up.email = usuario.email

        if usuario.email:
            usuario_up.email = usuario.email
        if usuario.admin:
            usuario_up.admin = usuario.admin

        await session.commit()

        return usuario_up


@router.patch(
    '/senha/{usuario_id}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=UsuarioSchema,
)
async def patch_usuario_senha(
    usuario_id: int,
    usuario: UsuarioUpdateSenha,
    session: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user),
):
    async with session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_up: UsuarioModel = result.scalars().unique().one_or_none()

        if not usuario_up:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Usuario não encontrado',
            )
        # TODO: melhorar este filtro
        if usuario.senha:
            usuario_up.senha = usuario.senha

        await session.commit()

        return usuario_up


@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(
    usuario_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user),
):
    async with session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioModel = result.scalars().unique().one_or_none()

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Usuario não encontrado',
            )

        await session.delete(usuario)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post('/login')
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):

    usuario = await autenticar(
        email=form_data.username,
        senha=form_data.password,
        db=session,
    )

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Dados de acesso incorretos.',
        )

    return JSONResponse(
        content={
            'access_token': criar_token_acesso(sub=usuario.id),
            'token_type': 'Bearer',
        },
        status_code=status.HTTP_200_OK,
    )
