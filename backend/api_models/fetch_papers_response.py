from pydantic import BaseModel
from typing import List
from models.research_paper import ResearchPaper


class FetchPapersResponse(BaseModel):
    """Response model for fetch papers endpoint.
    
    Attributes:
        papers: List of research papers from the search
        total_results: Total number of papers found
        query: Original search query used
    """
    papers: List[ResearchPaper]
    total_results: int
    query: str
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "papers": [
                    {
                        "title": "Deep Learning: A Comprehensive Survey",
                        "authors": ["John Doe", "Jane Smith"],
                        "abstract": "This paper provides a comprehensive survey...",
                        "url": "https://arxiv.org/abs/example",
                        "published_date": "2024-03-23",
                        "source": "arxiv"
                    }
                ],
                "total_results": 1,
                "query": "deep learning"
            }
        } 