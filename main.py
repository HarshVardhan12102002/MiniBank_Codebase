from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .api.routes_account import router as account_router
from .api.routes_validation import router as validation_router
from .database import init_db
from .config import settings

app = FastAPI(
    title="MiniBank Onboarding API",
    description="Digital Savings Account Opening Platform – MiniBank",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "ERROR",
            "error": "INTERNAL_SERVER_ERROR",
            "message": str(exc),
            "path": request.url.path
        },
    )

app.include_router(validation_router)
app.include_router(account_router)

@app.get("/")
def root():
    return {"service": "MiniBank Onboarding", "version": "1.0.0", "status": "UP"}

@app.get("/health")
def health_check():
    return {"health": "OK"}
