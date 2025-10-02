"""
Minimal wrapper of DatasetBuilder for German Tax Law dataset generation.

This module provides CrewAI-compatible utilities for:
1. Building empty tree structures (inherited from DatasetBuilder)
2. Filtering trees to correct/incorrect versions based on legal elements

The legacy prompt-based generation methods have been replaced by CrewAI agents.
"""

from typing import List, Dict
from copy import deepcopy
import random

from src.dataset_builder import DatasetBuilder
from src.logic_tree.tree import LogicTree


class GermanTaxDataset(DatasetBuilder):
    """
    Minimal wrapper of DatasetBuilder for German Tax Law functionality.
    
    Used by CrewAI system to:
    - Build tree skeletons with empty nodes (via inherited build_structure())
    - Filter trees to correct/incorrect versions (via create_chapter_trees())
    
    Legacy methods (create_case_trees, create_chapter, prompt templates) have been
    removed as they are replaced by CrewAI agents in src/crews/.
    """

    def create_chapter_trees(self, case_trees: List[Dict]) -> List[Dict]:
        """
        Filter trees to create correct/incorrect versions based on legal elements.
        
        A correct tree includes all 3 German tax law elements:
        - Applicable law
        - Economic activity  
        - Procedural requirements
        
        An incorrect tree includes only 1-2 randomly selected elements.
        
        Args:
            case_trees: List of case dictionaries with 'tree', 'description', 'case_info'
            
        Returns:
            Updated case_trees with 'correct_tree' and 'incorrect_tree' added
        """
        for cidx, c in enumerate(case_trees):
            template = deepcopy(c['tree'])
            t = deepcopy(c['tree'])
            
            # Create incorrect tree: randomly sample 1-2 elements
            t.nodes[0].children = random.sample(
                [x for x in t.nodes[0].children], 
                random.randint(1, 2)
            )
            case_trees[cidx]['incorrect_tree'] = t
            
            # Create correct tree: keep only the 3 core legal elements
            case_trees[cidx]['correct_tree'] = deepcopy(c['tree'])
            case_trees[cidx]['correct_tree'].nodes[0].children = [
                x for x in template.nodes[0].children 
                if any([
                    keyword in x.value.lower() 
                    for keyword in ['applicable law', 'economic', 'procedural']
                ])
            ]
        
        return case_trees
