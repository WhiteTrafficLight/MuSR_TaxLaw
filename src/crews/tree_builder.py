"""
Tree structure building and expansion logic for German tax cases.
"""

from typing import Dict

from crewai import Agent

from src.logic_tree.tree import LogicTree, LogicNode, LogicNodeFactType
from src.dataset_types.german_tax_dataset import GermanTaxDataset
from src.crews.tasks import expand_node_with_crew, get_node_depth


def make_root_tree(case: Dict) -> LogicTree:
    """
    Create the root tree structure (depth 1) with three main branches:
    - Applicable law
    - Economic activity
    - Procedural requirements
    
    Args:
        case: Case dictionary with metadata
        
    Returns:
        LogicTree with root and three level-1 children
    """
    taxpayer = case.get('taxpayer', 'Taxpayer')
    tax_authority = case['tax_authority']
    final_decision = case['final_decision']
    
    # Determine labels based on states
    law_label = 'clear' if case['law_state'] == 'clear' else 'unclear'
    econ_label = 'sufficient' if case['econ_state'] == 'sufficient' else 'insufficient'
    proc_label = 'compliant' if case['proc_state'] == 'compliant' else 'deficient'

    root = LogicNode(
        f"{tax_authority} should {final_decision} the arrangement by {taxpayer}.", 
        [
            LogicNode(f"Applicable law is {law_label} for {taxpayer}'s arrangement."),
            LogicNode(f"Economic activity is {econ_label} for {taxpayer}'s operations."),
            LogicNode(f"Procedural requirements are {proc_label} for {taxpayer}'s application."),
        ], 
        frozen=True, 
        prunable=False
    )

    return LogicTree(nodes=[root], prune=False, populate=False)


def expand_tree_with_crew(
    tree_agent: Agent,
    creator: GermanTaxDataset,
    case: Dict,
    base_tree: LogicTree,
    use_model_validator: bool = False,
    model_validator_model = None,
    early_escape_model = None
) -> LogicTree:
    """
    Expand the tree structure using CrewAI agents.
    Each node at depth 1 and 2 is expanded using element-specific and level-specific prompts.
    
    Args:
        tree_agent: The tree expansion agent
        creator: GermanTaxDataset instance
        case: Case dictionary with metadata
        base_tree: Base tree with root and level-1 nodes
        use_model_validator: Whether to use LLM-based validation
        model_validator_model: Model for LLM validation
        early_escape_model: Cheaper model for initial validation
        
    Returns:
        Fully expanded LogicTree (depth 3)
    """
    # Build skeleton tree structure with empty nodes (like original dataset_builder)
    tree = creator.build_structure(
        depth=3, 
        bf_factor={2: 1.0}, 
        chance_to_prune=0.0, 
        chance_to_prune_all=0.0, 
        root_nodes=base_tree.nodes
    )

    def expand_tree_recursive(node: LogicNode, tree: LogicTree):
        """Recursively expand nodes using CrewAI."""
        depth = get_node_depth(node)
        if depth >= 3:  # Stop at depth 3
            return
        
        # Check if this node's children need values filled in
        if node.children and any(not child.value or child.value.strip() == '' for child in node.children):
            # Get LLM output for child values
            child_lines = expand_node_with_crew(
                tree_agent, 
                tree, 
                node, 
                case['description'], 
                case=case,
                use_model_validator=use_model_validator,
                model_validator_model=model_validator_model,
                early_escape_model=early_escape_model
            )
            
            # Parse output into facts
            facts_from_story = []
            commonsense_knowledge = []
            
            for line in child_lines:
                if '|' not in line:
                    continue
                    
                text = line.rsplit('|', 1)[0].strip()
                
                if '| Commonsense Knowledge' in line:
                    commonsense_knowledge.append(text)
                elif '| Fact From Story' in line or '| Complex Fact' in line:
                    facts_from_story.append(text)
            
            # Fill in child values based on their fact_type (already set by build_structure)
            try:
                for child in node.children:
                    if child.fact_type == LogicNodeFactType.COMMONSENSE:
                        if commonsense_knowledge:
                            child.value = commonsense_knowledge.pop(0)
                    elif child.fact_type == LogicNodeFactType.EXPLICIT:
                        if facts_from_story:
                            child.value = facts_from_story.pop(0)
            except Exception as e:
                print(f'ERROR filling child values: {e}')
                # Kill branch on error
                node.children = []
                return
        
        # Recursively expand children
        for child in node.children:
            expand_tree_recursive(child, tree)

    # Start expansion from level-1 nodes
    for root in tree.nodes:
        for child in root.children:
            expand_tree_recursive(child, tree)

    return tree

