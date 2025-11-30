import os
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from app.core.config import settings

class RAGService:
    def __init__(self):
        self.persist_directory = os.path.join(settings.DATA_DIR, "chroma_db")
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=settings.GOOGLE_API_KEY
        )
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name="sn_insight_docs"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def add_document(self, text: str, metadata: dict):
        """
        Chunks the text and adds it to the vector store.
        """
        if not text:
            return

        # Create Document objects
        docs = [Document(page_content=text, metadata=metadata)]
        
        # Split documents
        splits = self.text_splitter.split_documents(docs)
        
        # Add to vector store
        self.vector_store.add_documents(splits)
        # self.vector_store.persist() # Chroma 0.4+ persists automatically

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        return self.vector_store.similarity_search(query, k=k)

rag_service = RAGService()
