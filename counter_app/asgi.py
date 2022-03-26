import uvicorn
from .main import get_app

app = get_app()


def server():
    """Launched with `poetry run server` at root level"""
    uvicorn.run("counter_app.asgi:app", host="0.0.0.0", port=8000, reload=True)