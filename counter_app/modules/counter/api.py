import structlog
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from counter_app.containers import Container
from .service import CounterService

logger = structlog.get_logger()

router = APIRouter(prefix="/{key}")


@router.post("/")
@inject
async def increment(key: str, service: CounterService = Depends(Provide[Container.counter_service])):
    value = await service.increment(key)
    logger.info('Counter incremented', key=key)
    return {"value": value}


@router.put("/")
@inject
async def reset(key: str, service: CounterService = Depends(Provide[Container.counter_service])):
    await service.set_value(key, 0)
    logger.info('Counter reseted', key=key)
    return {"value": 0}


@router.get("/")
@inject
async def get_key_value(
    key: str, service: CounterService = Depends(Provide[Container.counter_service])
):
    value = await service.get_value(key)
    return {"value": value}
