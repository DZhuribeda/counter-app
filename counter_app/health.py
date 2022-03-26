from fastapi import APIRouter


router = APIRouter()


@router.get("/healthz", response_model=str)
def health():
    return "OK"
