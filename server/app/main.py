import logging
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.routes.database import router as database_router
from app.api.routes.generate import router as generate_router

logger = logging.getLogger(__name__)

app = FastAPI(
    title="LazyQL API",
    description="Natural language to SQL API",
    version="1.0.0",
)

# Default allowed origins
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://lazyql.vercel.app",
]

# Support additional comma-separated origins from environment variable
custom_origins = os.getenv("ALLOWED_ORIGINS")
if custom_origins:
    origins.extend([origin.strip() for origin in custom_origins.split(",") if origin.strip()])


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            logger.exception("Unhandled server exception: %s", exc)
            return JSONResponse(
                status_code=500,
                content={"detail": f"Internal Server Error: {str(exc)}"},
            )


# Adding ErrorHandlingMiddleware first and CORSMiddleware second ensures
# CORSMiddleware wraps ErrorHandlingMiddleware, guaranteeing CORS headers
# on all responses (including 500 error responses).
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(database_router)
app.include_router(generate_router)


@app.get("/")
def health():
    return {
        "status": "ok",
        "service": "LazyQL",
    }