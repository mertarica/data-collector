from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router


def create_application() -> FastAPI:
    """Create FastAPI application with all configurations"""

    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="API for collecting and processing Spanish statistical data from INE",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # CORS Middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )

    # Include API router
    application.include_router(api_router, prefix=settings.API_V1_STR)

    return application


# Create app instance
app = create_application()


@app.get("/")
async def root():
    """Root endpoint with basic information"""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs": "/docs",
        "api": settings.API_V1_STR
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
