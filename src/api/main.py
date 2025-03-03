from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.database.config import connect_to_mongodb, close_mongodb_connection
from src.services.search_service import SearchService
from src.api.routers import section_router, search_router, toc_router

app = FastAPI(
    title="Criminal Code API",
    description="API for accessing and searching the Criminal Code of Canada",
    version="0.1.0",
)

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handling
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"An unexpected error occurred: {str(exc)}"}
    )

# Database connection events
@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongodb()
    await SearchService.initialize()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongodb_connection()
    await SearchService.close()

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