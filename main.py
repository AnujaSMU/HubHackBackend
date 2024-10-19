import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.controller import (
    health_router,
    program_router,
    changes_router
)
app = FastAPI(
    title="ISANS Backend",
    version="v0.0.1"
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(program_router)
app.include_router(changes_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8011, reload=False)