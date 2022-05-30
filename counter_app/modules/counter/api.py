from edgedb import AsyncIOClient
from pydantic import BaseModel
import structlog
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse

from counter_app.metric import COUNTER_INCREMENT, COUNTER_RESET, COUNTER_READ
from counter_app.containers import Container
from counter_app.modules.auth.model import User
from counter_app.modules.auth.dependencies import get_required_user
from .model import AccessModeEnum
from .service import CounterService

logger = structlog.get_logger()

router = APIRouter(prefix="/api/v1")


class Counter(BaseModel):
    name: str
    initial_value: int | None = None
    access_mode: AccessModeEnum


class CreateCounter(Counter):
    initial_value: int | None = None


@router.post("/counter/")
@inject
async def create(
    counter: CreateCounter,
    current_user: User = Depends(get_required_user),
    service: CounterService = Depends(Provide[Container.counter.counter_service]),
):
    counter_id = await service.create(
        name=counter.name,
        initial_value=counter.initial_value,
        access_mode=counter.access_mode,
        owner_id=current_user.id,
    )
    return RedirectResponse(router.url_path_for("get", counter_id=counter_id))


@router.put("/counter/{counter_id}/", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def update(
    counter: Counter,
    counter_id: str,
    service: CounterService = Depends(Provide[Container.counter.counter_service]),
):
    await service.update(
        counter_id=counter_id,
        name=counter.name,
        access_mode=counter.access_mode,
    )


@router.get("/counter/{counter_id}/")
@inject
async def get(
    counter_id: str,
    edgedb_client: AsyncIOClient = Depends(Provide[Container.gateways.edgedb_client]),
):
    # TODO: check access mode
    counter = await edgedb_client.query_single(
        """
        SELECT Counter {id, name, created_at, owner_id, access_mode} FILTER .id = <uuid>$id
    """,
        id=counter_id,
    )
    return {
        "id": counter.id,
        "name": counter.name,
        "createdAt": counter.created_at,
        "ownerId": counter.owner_id,
        "accessMode": str(counter.access_mode),
    }


@router.delete("/counter/{counter_id}/", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete(
    counter_id: str,
    service: CounterService = Depends(Provide[Container.counter.counter_service]),
):
    # TODO: check access mode
    await service.delete(counter_id)


@router.post("/counterValue/{counter_id}/")
@inject
async def increment(
    counter_id: str,
    service: CounterService = Depends(Provide[Container.counter.counter_service]),
):
    value = await service.increment(counter_id)
    logger.info("Counter incremented", counter_id=counter_id)
    COUNTER_INCREMENT.labels(counter_name=counter_id).inc()
    return {"value": value}


@router.put("/counterValue/{counter_id}/")
@inject
async def reset(
    counter_id: str,
    service: CounterService = Depends(Provide[Container.counter.counter_service]),
):
    await service.set_value(counter_id, 0)
    logger.info("Counter reseted", counter_id=counter_id)
    COUNTER_RESET.labels(counter_name=counter_id).inc()
    return {"value": 0}


@router.get("/counterValue/{counter_id}/")
@inject
async def get_counter_id_value(
    counter_id: str,
    service: CounterService = Depends(Provide[Container.counter.counter_service]),
):
    value = await service.get_value(counter_id)
    COUNTER_READ.labels(counter_name=counter_id).inc()
    return {"value": value}
