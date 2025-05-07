from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.testclient import TestClient
from app.middleware.cors import add_cors_middleware

def test_add_cors_middleware():
    app = FastAPI()
    add_cors_middleware(app)
    middleware_classes = [middleware.cls for middleware in app.user_middleware]
    assert CORSMiddleware in middleware_classes

def test_cors_allow_origins():
    app = FastAPI()
    add_cors_middleware(app)

    @app.get("/")
    def read_root():
        return {"message": "Hello World"}

    @app.options("/", include_in_schema=False)
    def options_root():
        return {}

    client = TestClient(app)

    response = client.options("/", headers={"Origin": "http://localhost"})

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost"




