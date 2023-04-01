from fastapi import APIRouter

from api.v1.endopoints import artigo, usuario


api_router = APIRouter()

api_router.include_router(artigo.router, prefix='/artigo', tags=['artigos'])
api_router.include_router(usuario.router, prefix='/usuario', tags=['usuarios'])
