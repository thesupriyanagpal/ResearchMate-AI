from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.services.ingestion import ingestion_service

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url=f"{settings.API_PREFIX}/docs",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to ResearchMate AI API"}

@app.post(f"{settings.API_PREFIX}/upload")
async def upload_document(file: UploadFile = File(...)):
    result = await ingestion_service.process_document(file)
    return result

from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

@app.post(f"{settings.API_PREFIX}/query")
async def query_agent(request: QueryRequest):
    from app.agents.orchestrator import orchestrator
    result = await orchestrator.process_query(request.query)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
