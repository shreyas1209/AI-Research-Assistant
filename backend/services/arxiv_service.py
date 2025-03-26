from config.settings import get_settings
import httpx
from typing import Dict, Any, List
from utils.logger import get_logger
from utils.async_retry import async_retry
import asyncio
import xml.etree.ElementTree as ET
from datetime import datetime
from models.research_paper import ResearchPaper

logger = get_logger(__name__)
settings = get_settings()


class ArxivService:
    """Service for interacting with ArXiv API."""
    
    # ArXiv XML namespaces
    ATOM_NS = {'atom': 'http://www.w3.org/2005/Atom',
               'arxiv': 'http://arxiv.org/schemas/atom'}
    
    def __init__(self):
        self._base_url = settings.ARXIV_URL
        self._client = httpx.AsyncClient(
            timeout=30.0,
            limits=httpx.Limits(
                max_keepalive_connections=5,
                max_connections=10,
                keepalive_expiry=30.0
            )
        )
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.aclose()
    
    @async_retry(retries=3, delay=1.0, backoff=2.0, exceptions=(httpx.HTTPError, asyncio.TimeoutError))
    async def fetch_papers(
        self,
        query: str,
        max_results: int = 10,
        sort_by: str = "submittedDate",
        sort_order: str = "descending"
    ) -> List[ResearchPaper]:
        """Fetch papers from ArXiv with retry logic.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            sort_by: Field to sort by (submittedDate, relevance, lastUpdatedDate)
            sort_order: Sort direction (ascending or descending)
            
        Returns:
            List of ResearchPaper objects
            
        Raises:
            httpx.HTTPError: If the request fails after all retries
            ValueError: If invalid parameters are provided
            ET.ParseError: If XML parsing fails
        """
        # Validate parameters
        valid_sort_by = {"submittedDate", "relevance", "lastUpdatedDate"}
        valid_sort_order = {"ascending", "descending"}
        
        if sort_by not in valid_sort_by:
            raise ValueError(f"sort_by must be one of {valid_sort_by}")
        if sort_order not in valid_sort_order:
            raise ValueError(f"sort_order must be one of {valid_sort_order}")
        
        try:
            params = {
                "search_query": query,
                "max_results": max_results,
                "sortBy": sort_by,
                "sortOrder": sort_order
            }
            
            response = await self._client.get(
                self._base_url,
                params=params
            )
            response.raise_for_status()
            
            return self._parse_response(response.text)
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred while searching ArXiv: {str(e)}")
            raise
        except ET.ParseError as e:
            logger.error(f"Failed to parse ArXiv XML response: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error occurred while searching ArXiv: {str(e)}")
            raise
    
    def _parse_response(self, xml_text: str) -> List[ResearchPaper]:
        """Parse ArXiv API XML response into ResearchPaper objects.
        
        Args:
            xml_text: Raw XML response from ArXiv API
            
        Returns:
            List of ResearchPaper objects
            
        Raises:
            ET.ParseError: If XML parsing fails
        """
        try:
            root = ET.fromstring(xml_text)
            papers = []
            
            for entry in root.findall('atom:entry', self.ATOM_NS):
                # Extract basic metadata
                title = entry.find('atom:title', self.ATOM_NS).text.strip()
                abstract = entry.find('atom:summary', self.ATOM_NS).text.strip()
                
                # Extract authors
                authors = [
                    author.find('atom:name', self.ATOM_NS).text.strip()
                    for author in entry.findall('atom:author', self.ATOM_NS)
                ]
                
                # Extract URL (prefer DOI if available)
                url = entry.find('atom:id', self.ATOM_NS).text.strip()
                doi_links = entry.findall("atom:link[@title='doi']", self.ATOM_NS)
                if doi_links:
                    url = doi_links[0].get('href')
                
                # Extract and format publication date
                published = entry.find('atom:published', self.ATOM_NS).text
                published_date = datetime.fromisoformat(published).strftime('%Y-%m-%d')
                
                # Create ResearchPaper object
                paper = ResearchPaper(
                    title=title,
                    authors=authors,
                    abstract=abstract,
                    url=url,
                    published_date=published_date,
                    source="arxiv"
                )
                papers.append(paper)
            
            logger.info(f"Successfully parsed {len(papers)} papers from ArXiv response")
            return papers
            
        except ET.ParseError as e:
            logger.error(f"XML parsing error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error parsing ArXiv response: {str(e)}")
            raise
    