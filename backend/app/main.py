from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AI Research Assistant is Running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}