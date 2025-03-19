from fastapi import FastAPI, Request

from app.api import routes
from app.database.session import engine, Base
import logging

#Str + NumPad /   für un/comment

Base.metadata.create_all(bind=engine)

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ])

#Logs von Uvicorn rausnehmen, da ich erstmal nur die API-Logs sehen möchte
logging.getLogger("uvicorn").propagate = False
logging.getLogger("uvicorn.error").propagate = False
logging.getLogger("uvicorn.access").propagate = False
logging.getLogger("uvicorn.error").setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)

app.include_router(routes.router, tags=["tasks"]) #Tags steht hier für Swagger zum gruppieren

@app.middleware("http")
async def log_requests(request: Request, call_next):
    ignored_paths = {"/favicon.ico", "/openapi.json", "/docs", "/redoc"}
    if request.url.path in ignored_paths:
        return await call_next(request)
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

@app.get("/")
def read_root():
    return {"message": "Please visit /docs for Swagger documentation"}

