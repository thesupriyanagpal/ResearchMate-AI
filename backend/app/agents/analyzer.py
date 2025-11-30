from typing import Any, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from app.agents.base import BaseAgent
from app.services.rag import rag_service
from app.core.config import settings

class PaperAnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Paper Analyzer",
            description="Extracts summaries, methodologies, and key findings from research papers."
        )
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.7
        )

    async def run(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        # 1. Retrieve relevant context from RAG
        docs = rag_service.similarity_search(query)
        context_text = "\n\n".join([d.page_content for d in docs])

        # 2. Construct Prompt
        prompt = PromptTemplate(
            input_variables=["context", "query"],
            template="""
            You are an expert research assistant. Use the following context from a research paper to answer the user's request.
            
            Context:
            {context}
            
            User Request:
            {query}
            
            Provide a structured and detailed response.
            """
        )
        
        chain = prompt | self.llm

        # 3. Generate Response
        response = await chain.ainvoke({"context": context_text, "query": query})
        
        return {
            "agent": self.name,
            "response": response.content,
            "sources": [d.metadata.get("source") for d in docs]
        }
