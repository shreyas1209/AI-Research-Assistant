from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from services.arxiv_service import ArxivService
from models.research_paper import ResearchPaper
from api_models.fetch_papers_response import FetchPapersResponse
from utils.logger import get_logger


class FetchPapersRouter:
    """Router for fetching research papers."""
    
    def __init__(self):
        self.router = APIRouter()
        self.logger = get_logger(__name__)
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup the fetch papers route."""
        @self.router.get("/fetch", response_model=FetchPapersResponse)
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
                self.logger.info(f"Fetching papers with query: {query}, max_results: {max_results}")
                
                async with ArxivService() as arxiv:
                    papers = await arxiv.fetch_papers(
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
                    
                    self.logger.info(f"Successfully fetched {len(papers)} papers")
                    return response
                    
            except ValueError as e:
                self.logger.error(f"Invalid parameters: {str(e)}")
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                self.logger.error(f"Error fetching papers: {str(e)}")
                raise HTTPException(status_code=500, detail="Failed to fetch papers")


# Create singleton instance
fetch_papers_router = FetchPapersRouter() 