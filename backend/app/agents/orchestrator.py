from typing import Any, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from app.core.config import settings
from app.agents.analyzer import PaperAnalyzerAgent
from app.agents.insight import InsightGeneratorAgent
from app.agents.comparator import PaperComparisonAgent
from app.agents.codegen import CodeGeneratorAgent
from app.agents.dashboard import DashboardPlannerAgent
from app.agents.writer import DocumentationWriterAgent

class AgentSelection(BaseModel):
    agent_name: str = Field(description="The name of the agent to select.")
    reason: str = Field(description="The reason for selecting this agent.")

class OrchestratorAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.3
        )
        self.agents = {
            "Paper Analyzer": PaperAnalyzerAgent(),
            "Insight Generator": InsightGeneratorAgent(),
            "Paper Comparator": PaperComparisonAgent(),
            "Code Generator": CodeGeneratorAgent(),
            "Dashboard Planner": DashboardPlannerAgent(),
            "Documentation Writer": DocumentationWriterAgent(),
        }
        self.parser = PydanticOutputParser(pydantic_object=AgentSelection)

    async def route_query(self, query: str) -> str:
        agent_descriptions = "\n".join([f"- {name}: {agent.description}" for name, agent in self.agents.items()])
        
        prompt = PromptTemplate(
            input_variables=["query", "agent_descriptions"],
            template="""
            You are the Master Orchestrator. Your job is to select the best agent to handle the user's request.
            
            Available Agents:
            {agent_descriptions}
            
            User Request:
            {query}
            
            Select the most appropriate agent name from the list above.
            {format_instructions}
            """,
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
        chain = prompt | self.llm | self.parser
        try:
            selection = await chain.ainvoke({"query": query, "agent_descriptions": agent_descriptions})
            return selection.agent_name
        except Exception as e:
            print(f"Routing error: {e}. Defaulting to Paper Analyzer.")
            return "Paper Analyzer"

    async def process_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        # 1. Route
        agent_name = await self.route_query(query)
        
        # 2. Select Agent
        agent = self.agents.get(agent_name)
        if not agent:
            agent = self.agents["Paper Analyzer"] # Fallback
            
        # 3. Execute
        try:
            result = await agent.run(query, context)
            return result
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                print(f"Quota exceeded during agent execution: {e}")
                return {
                    "answer": "I apologize, but I've hit the usage limits for the Google Gemini API (Free Tier). Please try again in a minute or check your quota.",
                    "agent": agent_name,
                    "status": "error_quota_exceeded"
                }
            else:
                print(f"Error during agent execution: {e}")
                return {
                    "answer": f"I encountered an error while processing your request: {str(e)}",
                    "agent": agent_name,
                    "status": "error"
                }

orchestrator = OrchestratorAgent()
