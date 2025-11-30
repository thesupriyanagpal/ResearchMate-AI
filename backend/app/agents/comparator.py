from typing import Any, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from app.agents.base import BaseAgent
from app.services.rag import rag_service
from app.core.config import settings

class PaperComparisonAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Paper Comparator",
            description="Compares multiple papers on methodology, results, and metrics."
        )
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.7
        )

    async def run(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        # For comparison, we might need to retrieve more documents or specific ones
        docs = rag_service.similarity_search(query, k=6) 
        context_text = "\n\n".join([d.page_content for d in docs])

        prompt = PromptTemplate(
            input_variables=["context", "query"],
            template="""
            You are a meticulous reviewer. Compare the research papers discussed in the context.
            Focus on:
            - Methodology
            - Datasets used
            - Performance Metrics
            - Results
            
            Context:
            {context}
            
            User Request:
            {query}
            
            Provide a comparison table (Markdown) and a narrative summary.
            """
        )
        
        chain = prompt | self.llm
        response = await chain.ainvoke({"context": context_text, "query": query})
        
        return {
            "agent": self.name,
            "response": response.content,
            "sources": [d.metadata.get("source") for d in docs]
        }
