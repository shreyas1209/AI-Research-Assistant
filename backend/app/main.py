from fastapi import FastAPI
from utils.logger import get_logger
from routers.fetch_papers_router import fetch_papers_router

# Initialize logger
logger = get_logger(__name__)

app = FastAPI(
    title="AI Research Assistant API",
    description="API for fetching and analyzing research papers",
    version="1.0.0"
)

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "AI Research Assistant is Running"}

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down")
# Include the fetch papers router
app.include_router(fetch_papers_router.router, prefix="/arxiv", tags=["arxiv"])
