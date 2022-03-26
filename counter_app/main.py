from fastapi import FastAPI

def get_app():
    app = FastAPI(title="Counter App")
    return app
