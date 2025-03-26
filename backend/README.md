# AI Research Assistant Backend

This is the backend service for the AI Research Assistant project. It provides APIs for fetching and analyzing research papers.

## Setup

1. Install dependencies:
```bash
poetry install
```

2. Run the service:
```bash
poetry run uvicorn app.main:app --reload
```

## API Endpoints

- `/fetch`: Fetch research papers from ArXiv
- `/health`: Health check endpoint 