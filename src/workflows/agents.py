import os
from crewai import Agent
from typing import Optional

from src.config.config_loader import ConfigLoader
# from src.tools.rag_tool import RAGTool
# from src.tools.memory_tool import MemoryTool
# from src.tools.arxiv_tool import ArxivTool
# from src.tools.web_search_tool import FirecrawlSearchTool
from src.tools import RAGTool, MemoryTool, ArxivTool, FirecrawlSearchTool
from src.rag.rag_pipeline import RAGPipeline
from src.memory.memory import ZepMemoryLayer


class Agents:
    """Class for creating agents from configuration files"""
    def __init__(self, config_loader: Optional[ConfigLoader] = None):
        self.config_loader = config_loader or ConfigLoader()
    
    def create_rag_agent(self, rag_pipeline: RAGPipeline) -> Agent:
        config = self.config_loader.get_agent_config("rag_agent")
        rag_tool = RAGTool(rag_pipeline=rag_pipeline)
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            llm="gemini/gemini-2.5-flash-lite",
            tools=[rag_tool],
            verbose=config.get("verbose", True)
        )
    
    def create_memory_agent(self, memory_layer: ZepMemoryLayer) -> Agent:
        config = self.config_loader.get_agent_config("memory_agent")
        memory_tool = MemoryTool(memory_layer=memory_layer)
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            llm="gemini/gemini-2.5-flash-lite",
            tools=[memory_tool],
            verbose=config.get("verbose", True)
        )
    
    def create_web_search_agent(self, firecrawl_api_key: str) -> Agent:
        config = self.config_loader.get_agent_config("web_search_agent")
        web_search_tool = FirecrawlSearchTool(api_key=firecrawl_api_key)
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            llm="gemini/gemini-2.5-flash-lite",
            tools=[web_search_tool],
            verbose=config.get("verbose", True)
        )
    
    def create_arxiv_agent(self) -> Agent:
        config = self.config_loader.get_agent_config("arxiv_agent")
        arxiv_tool = ArxivTool()
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            llm="gemini/gemini-2.5-flash-lite",
            tools=[arxiv_tool],
            verbose=config.get("verbose", True)
        )
    
    def create_evaluator_agent(self) -> Agent:
        config = self.config_loader.get_agent_config("evaluator_agent")
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            llm="gemini/gemini-2.5-flash-lite",
            verbose=config.get("verbose", True)
        )
    
    def create_synthesizer_agent(self) -> Agent:
        config = self.config_loader.get_agent_config("synthesizer_agent")
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            llm="gemini/gemini-2.5-flash-lite",
            verbose=config.get("verbose", True)
        )