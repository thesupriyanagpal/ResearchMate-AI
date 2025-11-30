import pytest
from app.services.rag import RAGService
from app.core.config import settings

class TestRAGService:
    """Test RAG service functionality"""
    
    def test_rag_initialization(self):
        """Test that RAG service initializes correctly"""
        rag = RAGService()
        assert rag.embeddings is not None
        assert rag.vector_store is not None
        assert rag.text_splitter is not None
    
    def test_add_document(self, sample_text):
        """Test adding a document to the vector store"""
        rag = RAGService()
        
        # Add document
        rag.add_document(sample_text, {"source": "test_paper.pdf"})
        
        # Verify we can search for it
        results = rag.similarity_search("transformer architecture", k=2)
        assert len(results) > 0
        assert "Transformer" in results[0].page_content or "transformer" in results[0].page_content
    
    def test_similarity_search(self, sample_text):
        """Test similarity search functionality"""
        rag = RAGService()
        rag.add_document(sample_text, {"source": "test_paper.pdf"})
        
        # Search for relevant content
        results = rag.similarity_search("BLEU score results", k=3)
        assert len(results) > 0
        
        # Check that results contain relevant information
        combined_text = " ".join([doc.page_content for doc in results])
        assert "BLEU" in combined_text or "results" in combined_text.lower()
    
    def test_empty_text_handling(self):
        """Test that empty text is handled gracefully"""
        rag = RAGService()
        
        # Should not raise an error
        rag.add_document("", {"source": "empty.pdf"})
        
        # Search should still work
        results = rag.similarity_search("test query")
        # Results might be empty or contain previous test data
        assert isinstance(results, list)
