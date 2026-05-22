"""FastAPI backend for DealMind - Real Estate AI Underwriting Platform"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config.settings import settings
from app.api import auth, deals, underwriting, chat, reports


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("DealMind Backend Starting...")
    yield
    # Shutdown
    print("DealMind Backend Shutting Down...")


app = FastAPI(
    title="DealMind API",
    description="AI Real Estate Underwriting Platform",
    version="0.1.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "DealMind Backend",
        "version": "0.1.0"
    }


# API Routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(deals.router, prefix="/api/deals", tags=["deals"])
app.include_router(underwriting.router, prefix="/api/underwriting", tags=["underwriting"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
