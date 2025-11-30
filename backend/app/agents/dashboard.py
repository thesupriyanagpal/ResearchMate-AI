from typing import Any, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from app.agents.base import BaseAgent
from app.services.rag import rag_service
from app.core.config import settings

class DashboardPlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Dashboard Planner",
            description="Suggests KPIs, charts, and layout for visualizing research data."
        )
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.7
        )

    async def run(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        docs = rag_service.similarity_search(query)
        context_text = "\n\n".join([d.page_content for d in docs])

        prompt = PromptTemplate(
            input_variables=["context", "query"],
            template="""
            You are a Data Visualization Expert. Plan a dashboard to visualize the findings or data from the research paper.
            
            Context:
            {context}
            
            User Request:
            {query}
            
            Suggest:
            1. Key Performance Indicators (KPIs)
            2. Chart Types (Bar, Line, Scatter, Heatmap, etc.)
            3. Layout Structure
            4. Titles and Descriptions
            """
        )
        
        chain = prompt | self.llm
        response = await chain.ainvoke({"context": context_text, "query": query})
        
        return {
            "agent": self.name,
            "response": response.content,
            "sources": [d.metadata.get("source") for d in docs]
        }
