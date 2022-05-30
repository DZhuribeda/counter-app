from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from starlette.status import HTTP_401_UNAUTHORIZED

from counter_app.containers import Container

from .service import AuthenticationService
from .model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


@inject
async def get_optional_user(
    service: AuthenticationService = Depends(Provide[Container.authentication_service]),
    token: str = Depends(oauth2_scheme),
) -> User | None:
    user = service.decode_token(token)
    return user


@inject
async def get_required_user(
    user: User | None = Depends(get_optional_user),
) -> User | None:
    if user is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
