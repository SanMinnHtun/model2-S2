"""FastAPI application for Model 2: IT Career Diagnostic."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.career_quiz import router as career_quiz_router

app = FastAPI(title="Model 2: IT Career Diagnostic", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(career_quiz_router)


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "Model 2: IT Career Diagnostic"}
