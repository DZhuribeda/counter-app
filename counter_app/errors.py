from fastapi import APIRouter
import structlog


router = APIRouter()

logger = structlog.get_logger()


@router.get("/handled", response_model=str)
def handled():
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("Exception handled")
    return "OK"


@router.get("/unhandled", response_model=str)
def unhandled():
    1 / 0
    return "OK"
