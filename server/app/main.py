import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.database import router as database_router
from app.api.routes.generate import router as generate_router


app = FastAPI()

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