from fastapi import FastAPI, Query, HTTPException
from utils.logger import get_logger
from typing import List, Optional
from services.arxiv_service import ArxivService
from models.research_paper import ResearchPaper
from pydantic import BaseModel
from api_models.fetch_papers_response import FetchPapersResponse

# Initialize logger
logger = get_logger(__name__)

app = FastAPI(
    title="AI Research Assistant API",
    description="API for fetching and analyzing research papers",
    version="1.0.0"
)

class FetchPapersResponse(BaseModel):
    """Response model for fetch papers endpoint."""
    papers: List[ResearchPaper]
    total_results: int
    query: str

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "AI Research Assistant is Running"}

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy"}

@app.get("/fetch", response_model=FetchPapersResponse)
async def fetch_papers(
    query: str = Query(..., description="Search query for papers"),
    max_results: Optional[int] = Query(10, ge=1, le=100, description="Maximum number of results to return"),
    sort_by: Optional[str] = Query(
        "submittedDate",
        description="Field to sort by",
        enum=["submittedDate", "relevance", "lastUpdatedDate"]
    ),
    sort_order: Optional[str] = Query(
        "descending",
        description="Sort direction",
        enum=["ascending", "descending"]
    )
) -> FetchPapersResponse:
    """Fetch research papers from ArXiv.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (1-100)
        sort_by: Field to sort by (submittedDate, relevance, lastUpdatedDate)
        sort_order: Sort direction (ascending or descending)
        
    Returns:
        FetchPapersResponse containing list of papers and metadata
        
    Raises:
        HTTPException: If the request fails or returns invalid data
    """
    try:
        logger.info(f"Fetching papers with query: {query}, max_results: {max_results}")
        
        async with ArxivService() as arxiv:
            papers = await arxiv.search_papers(
                query=query,
                max_results=max_results,
                sort_by=sort_by,
                sort_order=sort_order
            )
            
            response = FetchPapersResponse(
                papers=papers,
                total_results=len(papers),
                query=query
            )
            
            logger.info(f"Successfully fetched {len(papers)} papers")
            return response
            
    except ValueError as e:
        logger.error(f"Invalid parameters: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching papers: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch papers")

@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down")