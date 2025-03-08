# AI Research Assistant

A full-stack AI-powered research assistant application.

## Backend Setup

1. Copy the environment template:
```bash
cd backend
cp .env.example .env
```

2. Update the `.env` file with your actual values:
- Replace `your_openai_api_key_here` with your OpenAI API key
- Replace `your_huggingface_api_key_here` with your HuggingFace API key
- Adjust other settings as needed

3. Install and run:
```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

The backend server will be available at `http://localhost:8000`

## Project Structure
```
.
├── backend/             # FastAPI backend
│   ├── app/            # Application code
│   ├── .env.example    # Environment template
│   └── pyproject.toml  # Python dependencies
└── README.md           # This file
```
