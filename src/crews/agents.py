"""
CrewAI agent definitions for German tax case generation.
"""

from crewai import Agent
from langchain_openai import ChatOpenAI

from src.crews.prompts import TREE_AGENT_SYSTEM_PROMPT, STORY_AGENT_SYSTEM_PROMPT


def create_tree_agent(model: str = "gpt-4", temperature: float = 1.0) -> Agent:
    """
    Create the tree expansion agent responsible for generating child nodes.
    
    Args:
        model: OpenAI model name
        temperature: Sampling temperature
        
    Returns:
        CrewAI Agent configured for tree expansion
    """
    llm = ChatOpenAI(model=model, temperature=temperature)
    
    return Agent(
        role="German Tax Law Reasoning Tree Expander",
        goal="Generate child nodes (2 Fact From Story + 1 Commonsense Knowledge) that entail the parent deduction",
        backstory=TREE_AGENT_SYSTEM_PROMPT,
        llm=llm,
        verbose=True
    )


def create_story_agent(model: str = "gpt-4", temperature: float = 1.0) -> Agent:
    """
    Create the story generation agent responsible for writing court decision sections.
    
    Args:
        model: OpenAI model name
        temperature: Sampling temperature
        
    Returns:
        CrewAI Agent configured for story generation
    """
    llm = ChatOpenAI(model=model, temperature=temperature)
    
    return Agent(
        role="German Tax Court Document Writer",
        goal="Write formal court decision sections that present facts objectively without revealing the judgment",
        backstory=STORY_AGENT_SYSTEM_PROMPT,
        llm=llm,
        verbose=True
    )

