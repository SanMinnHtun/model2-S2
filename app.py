"""FastAPI application for Model 2: IT Career Diagnostic."""

from contextlib import asynccontextmanager
from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.career_quiz import load_model, model_is_loaded, router as career_quiz_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Load once at startup instead of reading the artifact on every prediction.
    load_model()
    yield


app = FastAPI(title="The Way - Model 2 Career Diagnostic API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(career_quiz_router)


@app.get("/")
def health_check() -> dict[str, Union[str, bool]]:
    return {
        "status": "ok",
        "service": "The Way - Model 2 Career Diagnostic API",
        "model_loaded": model_is_loaded(),
    }
