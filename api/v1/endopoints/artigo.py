from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from models.artigo import Artigo as ArtigoModel
from models.usuario import Usuario as UsuarioModel
from schemas.artigo import Artigo as ArtigoSchema
from schemas.usuario import Usuario as UsuarioSchema

from core.common import get_session, get_current_user

router = APIRouter()


@router.post(
    '/', status_code=status.HTTP_201_CREATED, response_model=ArtigoSchema
)
async def create_artigo(
    artigo: ArtigoSchema,
    session: AsyncSession = Depends(get_session),
    usuario: UsuarioModel = Depends(get_current_user),
):
    novo_artigo: ArtigoModel = ArtigoModel(
        usuario_id=usuario.id, **artigo.dict()
    )

    session.add(novo_artigo)
    await session.commit()

    return novo_artigo


@router.get(
    '/', status_code=status.HTTP_200_OK, response_model=List[ArtigoSchema]
)
async def read_all_artigos(
    session: AsyncSession = Depends(get_session),
):
    async with session:
        query = select(ArtigoModel)
        result = await session.execute(query)
        artigos: List[ArtigoModel] = result.scalars().unique().all()

        return artigos


@router.get(
    '/{artigo_id}', status_code=status.HTTP_200_OK, response_model=ArtigoSchema
)
async def read_artigo(
    artigo_id: int,
    session: AsyncSession = Depends(get_session),
):

    async with session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo: ArtigoModel = result.scalars().first()

        if not artigo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Artigo não encontrado',
            )


@router.patch(
    '/{artigo_id}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ArtigoSchema,
)
async def update_artigo(
    artigo_id: int,
    artigo: ArtigoSchema,
    session: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user),
):
    async with session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo_up: ArtigoModel = result.scalars().unique().one_or_none()

        if not artigo_up:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Artigo não encontrado',
            )

        # TODO: comparar os objetos e passar
        # só a difirença sem estes 'if'
        if artigo.titulo:
            artigo_up.titulo = artigo.titulo

        if artigo.descricao:
            artigo_up.descricao = artigo.descricao

            artigo_up.descricao = artigo.descricao

        if artigo.url_fonte:
            artigo_up.url_fonte = artigo.url_fonte

        if usuario_logado.id != artigo_up.usuario_id:
            artigo_up.usuario_id = usuario_logado.id
            # NOTE: Neste caso é permitido que um outro usuário edite o artigo
        await session.commit()

        return artigo_up


@router.delete('/{artigo}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_artigo(
    artigo_id: int,
    session: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user),
):
    async with session:
        query = (
            select(ArtigoModel)
            .filter(ArtigoModel.id == artigo_id)
            .filter(ArtigoModel.usuario_id == usuario_logado.id)
        )
        result = await session.execute(query)
        artigo: ArtigoModel = result.scalars().unique().one_or_none()

        if not artigo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Artigo não encontrado',
            )

        await session.delete(artigo)
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
