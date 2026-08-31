"""
FastAPI application entrypoint.

Run locally with:
    uvicorn main:app --reload

API docs are auto-generated at /docs once the server is running.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import Base, engine
from routers import dashboard, evaluate

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ControlPlane.ai",
    description="A model-agnostic control layer for enterprise AI.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(evaluate.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "ControlPlane.ai backend"}


@app.get("/health")
def health():
    return {"status": "healthy"}
