import uvicorn
from fastapi.responses import RedirectResponse
from app import *
from routers import brands


@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url="/docs")


app.include_router(
    brands.router,
    prefix="/api/v1/brands",
    tags=["brands"],
)

if __name__ == "__main__":
    # Use this for debugging purposes only
    uvicorn.run(
        "main:app", host="0.0.0.0", port=8000, log_level=LOG_LEVEL, reload=RELOAD
    )
