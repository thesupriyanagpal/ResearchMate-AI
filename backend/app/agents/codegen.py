from typing import Any, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from app.agents.base import BaseAgent
from app.services.rag import rag_service
from app.core.config import settings

class CodeGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Code Generator",
            description="Generates Python code for EDA, ML models, and data processing."
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
            You are an expert Machine Learning Engineer. Generate Python code based on the research paper's methodology or the user's request.
            
            Context:
            {context}
            
            User Request:
            {query}
            
            Rules:
            - Return ONLY valid Python code inside markdown code blocks.
            - Include comments explaining the steps.
            - Use standard libraries (pandas, numpy, sklearn, matplotlib, torch/tensorflow).
            """
        )
        
        chain = prompt | self.llm
        response = await chain.ainvoke({"context": context_text, "query": query})
        
        return {
            "agent": self.name,
            "response": response.content,
            "sources": [d.metadata.get("source") for d in docs]
        }
