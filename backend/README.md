# AI Research Assistant Backend

## Environment Setup

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Update the `.env` file with your actual values:
- Replace `your_openai_api_key_here` with your OpenAI API key
- Replace `your_huggingface_api_key_here` with your HuggingFace API key
- Adjust other settings as needed

## Installation

```bash
# Install dependencies
poetry install

# Start the server
poetry run uvicorn app.main:app --reload
```
