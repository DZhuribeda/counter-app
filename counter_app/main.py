import logging
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.b3 import B3Format


from counter_app.modules.health import api as health_api
from counter_app.modules.counter import api as counter_api
from counter_app.modules.errors import api as errors_api
from counter_app.containers import Container
from counter_app.logging import logging_setup


def get_app():
    app = FastAPI(title="Counter App")
    app.include_router(health_api.router)
    app.include_router(counter_api.router, prefix="/counter")
    app.include_router(errors_api.router, prefix="/errors")

    container = Container()
    container.config.redis_dsn.from_env(
        "REDIS_DNS", "redis://:password@localhost:6379/0"
    )
    container.config.redis_max_connections.from_env("REDIS_MAX_CONNECTIONS", 10)
    container.config.log_level.from_env("LOG_LEVEL", logging.INFO)
    container.config.log_json.from_env("LOG_JSON", False)

    container.wire(modules=[counter_api, health_api])

    @app.on_event("startup")
    async def startup_event():
        await container.init_resources()

    @app.on_event("shutdown")
    async def shutdown_event():
        await container.shutdown_resources()

    Instrumentator(should_respect_env_var=True).instrument(app).expose(app)
    set_global_textmap(B3Format())
    logging_setup(container.config)

    return app
