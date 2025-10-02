"""
CrewAI-based German tax case generation module.

This module provides a clean separation of concerns:
- agents: Agent creation (tree expansion and story generation)
- tasks: Task creation and node expansion logic
- scenario: Scenario sampling and case building
- tree_builder: Tree structure creation and expansion
- html_renderer: HTML visualization
- runner: Main orchestration
"""

from src.crews.agents import create_tree_agent, create_story_agent
from src.crews.runner import run_single_german_tax_case

__all__ = [
    'create_tree_agent',
    'create_story_agent',
    'run_single_german_tax_case',
]

