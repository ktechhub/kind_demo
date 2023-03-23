from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from config import *

description = """
DemoFastapi API helps you interact with endpoints . 🚀
"""

app = FastAPI(
    title="DemoFastapi APIs",
    openapi_url="/openapi.json",
    description=description,
    version=api_version,
    contact=contact,
    terms_of_service="https://demofastapi.com/terms/",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/readyz", status_code=status.HTTP_200_OK, include_in_schema=False)
async def readyz() -> str:
    """Check if is ready"""
    return "ready"


@app.get("/livez", status_code=status.HTTP_200_OK, include_in_schema=False)
async def livez() -> str:
    """Check if is live"""
    return "live"
