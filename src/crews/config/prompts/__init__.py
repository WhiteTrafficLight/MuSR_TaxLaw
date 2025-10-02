"""
Prompt configuration for tree expansion agents.
"""

from .law import LAW_L1_L2, LAW_L2_L3
from .econ import ECON_L1_L2, ECON_L2_L3
from .proc import PROC_L1_L2, PROC_L2_L3
from .story import STORY_GENERATION_PROMPT

__all__ = [
    'LAW_L1_L2',
    'LAW_L2_L3',
    'ECON_L1_L2',
    'ECON_L2_L3',
    'PROC_L1_L2',
    'PROC_L2_L3',
    'STORY_GENERATION_PROMPT',
]

