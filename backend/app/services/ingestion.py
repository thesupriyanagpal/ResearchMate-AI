import os
import shutil
from typing import List
from fastapi import UploadFile
import pdfplumber
from app.core.config import settings

class IngestionService:
    def __init__(self):
        self.upload_dir = os.path.join(settings.DATA_DIR, "uploads")
        os.makedirs(self.upload_dir, exist_ok=True)

    async def save_upload(self, file: UploadFile) -> str:
        file_path = os.path.join(self.upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_path

    def extract_text(self, file_path: str) -> str:
        text_content = []
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
        except Exception as e:
            print(f"Error extracting text from {file_path}: {e}")
            return ""
        
        return "\n".join(text_content)

    async def process_document(self, file: UploadFile):
        # 1. Save file
        file_path = await self.save_upload(file)
        
        # 2. Extract text
        text = self.extract_text(file_path)
        
        # 3. Chunking and Embedding (RAG)
        from app.services.rag import rag_service
        from fastapi import HTTPException
        
        try:
            rag_service.add_document(text, {"source": file.filename, "file_path": file_path})
            status = "ingested_and_indexed"
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                print(f"Quota exceeded during indexing: {e}")
                status = "ingested_only_quota_exceeded"
                # We don't raise an error here to allow the file to be saved/extracted
                # even if indexing fails. The user will be notified via status.
            else:
                print(f"Error during indexing: {e}")
                status = "ingested_only_indexing_failed"

        return {
            "filename": file.filename,
            "file_path": file_path,
            "text_length": len(text),
            "preview": text[:500] if text else "",
            "status": status,
            "warning": "Indexing failed due to API quota. Search may not work for this document." if "quota" in status else None
        }

ingestion_service = IngestionService()
