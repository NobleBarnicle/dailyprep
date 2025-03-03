from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time

from src.database.config import connect_to_mongodb, close_mongodb_connection
from src.services.search_service import SearchService
from src.api.routers import section_router, search_router, toc_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up API server")
    await connect_to_mongodb()
    await SearchService.initialize()
    
    yield
    
    # Shutdown
    logger.info("Shutting down API server")
    await close_mongodb_connection()
    await SearchService.close()

app = FastAPI(
    title="Criminal Code API",
    description="API for accessing and searching the Criminal Code of Canada",
    version="0.1.0",
    lifespan=lifespan,
)

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Process the request
    response = await call_next(request)
    
    # Log the request details
    process_time = (time.time() - start_time) * 1000
    logger.info(
        f"{request.client.host} - {request.method} {request.url.path} "
        f"- {response.status_code} - {process_time:.2f}ms"
    )
    
    return response

# Exception handling
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": f"An unexpected error occurred: {str(exc)}"}
    )

@app.get("/")
async def root():
    """Root endpoint that returns API information."""
    return {
        "message": "Welcome to the Criminal Code API",
        "version": "0.1.0",
        "docs_url": "/docs",
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}

# Include routers
app.include_router(section_router.router, prefix="/api/sections", tags=["sections"])
app.include_router(search_router.router, prefix="/api/search", tags=["search"])
app.include_router(toc_router.router, prefix="/api/table-of-contents", tags=["table-of-contents"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True) 