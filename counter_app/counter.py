import structlog
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from .containers import Container
from .services import Service

log = structlog.get_logger()

router = APIRouter(prefix="/{key}")


@router.post("/")
@inject
async def increment(key: str, service: Service = Depends(Provide[Container.service])):
    value = await service.increment(key)
    log.msg('Counter incremented', key=key)
    return {"value": value}


@router.put("/")
@inject
async def reset(key: str, service: Service = Depends(Provide[Container.service])):
    await service.set_value(key, 0)
    log.msg('Counter reseted', key=key)
    return {"value": 0}


@router.get("/")
@inject
async def get_key_value(
    key: str, service: Service = Depends(Provide[Container.service])
):
    value = await service.get_value(key)
    return {"value": value}
