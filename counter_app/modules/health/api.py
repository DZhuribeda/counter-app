from aioredis import Redis
from fastapi import APIRouter, Depends, Response, status
from dependency_injector.wiring import inject, Provide

from counter_app.containers import Container


router = APIRouter()


@router.get("/healthz", response_model=str)
def health():
    return "OK"


@router.get("/readyz")
@inject
async def readyz(
    response: Response, redis: Redis = Depends(Provide[Container.redis_pool])
):
    errors = []
    try:
        await redis.ping()
    except Exception as e:
        errors.append(
            {
                "service": "redis",
                "message": str(e),
            }
        )
    if len(errors):
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {"healthy": len(errors) == 0, "errors": errors}
