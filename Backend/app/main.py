from fastapi import FastAPI
from app.middleware.cors import add_cors_middleware
from app.routers import prediction
from app.utils.model_loader import preload_models
import uvicorn

app = FastAPI()

models_ready = False

def preload_and_set_ready():
    global models_ready
    preload_models()  
    models_ready = True

preload_and_set_ready()

add_cors_middleware(app)
app.include_router(prediction.router, prefix="/api")

@app.get("/ready")
def ready():
    return {"models_ready": models_ready}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
