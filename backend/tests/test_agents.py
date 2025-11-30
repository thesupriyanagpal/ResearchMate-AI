import pytest
from app.agents.base import BaseAgent
from app.agents.analyzer import PaperAnalyzerAgent
from app.agents.insight import InsightGeneratorAgent
from app.agents.orchestrator import OrchestratorAgent

class TestAgents:
    """Test agent functionality"""
    
    def test_analyzer_agent_initialization(self):
        """Test Paper Analyzer agent initializes correctly"""
        agent = PaperAnalyzerAgent()
        assert agent.name == "Paper Analyzer"
        assert agent.description is not None
        assert agent.llm is not None
    
    def test_insight_agent_initialization(self):
        """Test Insight Generator agent initializes correctly"""
        agent = InsightGeneratorAgent()
        assert agent.name == "Insight Generator"
        assert agent.description is not None
        assert agent.llm is not None
    
    def test_orchestrator_initialization(self):
        """Test Orchestrator initializes with all agents"""
        orchestrator = OrchestratorAgent()
        assert orchestrator.llm is not None
        assert len(orchestrator.agents) == 6
        assert "Paper Analyzer" in orchestrator.agents
        assert "Insight Generator" in orchestrator.agents
        assert "Code Generator" in orchestrator.agents
    
    @pytest.mark.asyncio
    async def test_orchestrator_routing(self):
        """Test that orchestrator can route queries"""
        orchestrator = OrchestratorAgent()
        
        # Test routing for analysis query
        agent_name = await orchestrator.route_query("Summarize this research paper")
        assert agent_name in orchestrator.agents.keys()
    
    @pytest.mark.asyncio
    async def test_agent_run_method_exists(self):
        """Test that agents have run method"""
        agent = PaperAnalyzerAgent()
        
        # Check that run method exists and is callable
        assert hasattr(agent, 'run')
        assert callable(agent.run)
