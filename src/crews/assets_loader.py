from typing import Any, Dict

from src.crews.config.prompts.law import LAW_L1_L2, LAW_L2_L3
from src.crews.config.prompts.econ import ECON_L1_L2, ECON_L2_L3
from src.crews.config.prompts.proc import PROC_L1_L2, PROC_L2_L3


def load_tree_prompts() -> Dict[str, Any]:
    """
    Load all tree prompts from config/prompts/*.py modules.
    Returns a dictionary with keys like 'law_l1_l2', 'econ_l2_l3', etc.
    """
    return {
        'law_l1_l2': LAW_L1_L2,
        'law_l2_l3': LAW_L2_L3,
        'econ_l1_l2': ECON_L1_L2,
        'econ_l2_l3': ECON_L2_L3,
        'proc_l1_l2': PROC_L1_L2,
        'proc_l2_l3': PROC_L2_L3,
    }


