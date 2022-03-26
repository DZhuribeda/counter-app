from fastapi import FastAPI

from counter_app import health


def get_app():
    app = FastAPI(title="Counter App")
    app.include_router(health.router)
    return app
