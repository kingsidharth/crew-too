import os

from crewai import Agent, LLM
from crewai_tools import TavilySearchTool

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def get_llm() -> LLM:
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if openrouter_key:
        return LLM(
            model=os.getenv("OPENROUTER_MODEL", "openrouter/google/gemini-2.5-flash"),
            api_key=openrouter_key,
            base_url=OPENROUTER_BASE_URL,
        )

    return LLM(model=os.getenv("OPENAI_MODEL", "gpt-4o"))


def create_search_agent(topic: str = "general", max_results: int = 5) -> Agent:
    search_tool = TavilySearchTool(
        max_results=max_results,
        search_depth="advanced",
        topic=topic,
    )

    return Agent(
        role="Senior Research Analyst",
        goal="Find accurate, comprehensive, and up-to-date information on any topic",
        backstory=(
            "You are a seasoned research analyst with expertise in synthesizing "
            "information from multiple sources. You excel at finding relevant data, "
            "identifying key trends, and presenting findings in a clear, structured format."
        ),
        tools=[search_tool],
        llm=get_llm(),
        verbose=True,
    )
