from pydantic import BaseModel
from typing import List

class ResearchPaper(BaseModel):
    title: str
    authors: List[str]
    abstract: str
    url: str
    published_date: str
    source: str

