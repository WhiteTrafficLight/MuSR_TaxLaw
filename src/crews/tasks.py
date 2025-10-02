"""
Task creation and node expansion logic for German tax case tree generation.
"""

from typing import List

from crewai import Agent, Task, Crew

from src.logic_tree.tree import LogicTree, LogicNode, LogicNodeFactType
from src.crews.assets_loader import load_tree_prompts
from src.validators import StructureValidator, ForbiddenTextValidator, ModelValidator, Validator
from src.model.openai import OpenAIModel


# Load prompts once at module level
_PROMPTS_ASSET = load_tree_prompts()


def get_node_depth(node: LogicNode) -> int:
    """Calculate the depth of a node in the tree."""
    depth = 0
    parent = node.parent
    while parent is not None:
        depth += 1
        parent = parent.parent
    return depth


def get_node_element(node: LogicNode) -> str:
    """
    Determine which legal element (law/econ/proc) this node belongs to.
    Traces up to the level-1 ancestor and checks its value.
    """
    current = node
    while current.parent is not None and current.parent.parent is not None:
        current = current.parent
    
    value = (current.value or '').lower()
    if 'applicable law' in value:
        return 'law'
    if 'economic' in value:
        return 'econ'
    if 'procedural' in value:
        return 'proc'
    return ''


def render_tree_state(tree: LogicTree) -> str:
    """Render the current tree state as a text representation."""
    lines = []
    
    def render_node(node: LogicNode, depth: int = 0):
        # Skip nodes without value
        if not node.value or not node.value.strip():
            return
            
        prefix = '> ' * depth
        lines.append(f"{prefix}{node.value}")
        for child in node.children:
            render_node(child, depth + 1)
    
    for root in tree.nodes:
        render_node(root)
    
    return "\n".join(lines)


def join_lines(value) -> str:
    """Helper to join list values into newline-separated string."""
    if isinstance(value, list):
        return "\n".join(value)
    return str(value)


def create_validators(
    node: LogicNode, 
    case: dict, 
    use_model_validator: bool = True,
    model_validator_model: OpenAIModel = None,
    early_escape_model: OpenAIModel = None
) -> List[Validator]:
    """
    Create validators for the node expansion.
    
    Args:
        node: Node being expanded (should have children with fact_type already set)
        case: Case metadata
        use_model_validator: Whether to use LLM-based validation (more accurate but expensive)
        model_validator_model: Main model for LLM validation
        early_escape_model: Cheaper model for initial validation attempt
        
    Returns:
        List of validators to apply
    """
    validators = [StructureValidator()]
    
    # Get node depth to apply level-specific validation
    depth = get_node_depth(node)
    
    # 1. Avoid conclusive words - level-specific intensity
    if depth <= 1:  # L1→L2: Strong constraints (prevent obvious conclusions)
        conclusive_words = [
            # Direct conclusions about element status (always forbidden at L1→L2)
            'sufficient', 'insufficient', 'compliant', 'non-compliant', 'deficient',
            'adequate', 'inadequate', 'appropriate', 'inappropriate',
            'satisfactory', 'unsatisfactory',
            
            # Strong conclusive adverbs
            'independently', 'entirely', 'completely', 'fully', 'clearly', 'obviously',
            'evidently', 'effectively', 'actively', 'substantially',
            'significantly', 'materially', 'extensively', 'comprehensively',
            
            # Strong conclusive adjectives
            'robust', 'substantial', 'significant',
            
            # Judgment verbs
            'properly', 'improperly', 'prove', 'confirm', 'validate', 'verify'
        ]
    else:  # L2→L3: Weaker constraints (allow concrete factual descriptions)
        conclusive_words = [
            # Only block the most direct conclusions at leaf level
            'sufficient', 'insufficient', 'compliant', 'non-compliant', 'deficient',
            'adequate', 'inadequate', 'appropriate', 'inappropriate',
            'satisfactory', 'unsatisfactory',
            'obviously', 'clearly', 'evidently', 'successfully','comprehensive','positive','negative'
        ]
    
    if conclusive_words:
        validators.append(ForbiddenTextValidator(
            forbidden_words=conclusive_words,
            reason_why="these words make the conclusion too obvious and reduce reasoning difficulty. Use neutral, factual language instead."
        ))
    
    # 2. Element purity: prevent cross-contamination between law/econ/proc branches
    element = get_node_element(node)
    
    if element == 'law':
        forbidden_words = [
            'economic', 'revenue', 'profit', 'income', 'investment', 'business development',
            'procedural', 'documentation', 'filing', 'submission', 'deadline', 'form'
        ]
    elif element == 'econ':
        forbidden_words = [
            'applicable law', 'treaty', 'statute', 'article', 'provision', 'legal framework',
            'procedural', 'documentation', 'filing', 'submission', 'deadline', 'form'
        ]
    elif element == 'proc':
        forbidden_words = [
            'applicable law', 'treaty', 'statute', 'article', 'provision', 'legal framework',
            'economic', 'revenue', 'profit', 'income', 'investment', 'business development'
        ]
    else:
        forbidden_words = []
    
    if forbidden_words:
        validators.append(ForbiddenTextValidator(
            forbidden_words=forbidden_words,
            reason_why=f"Element purity: the '{element}' branch must only contain facts about {element}, not other legal elements."
        ))
    
    # Optional: Add model-based validation (expensive but more accurate)
    if use_model_validator and model_validator_model:
        description = case.get('description', '')
        
        # Element-specific model validation prompts
        if element == 'law':
            validators.append(ModelValidator(
                model_validator_model,
                f"We are analyzing applicable law in a German tax case. Does this deduction in any way prove or help to prove economic activity (revenue, business operations) or procedural requirements (filing, documentation) given the case description below?\n\n{description}",
                "We are proving applicable law only. We do not want to prove economic activity or procedural requirements because that could make the reasoning complicated.",
                conditional='Applicable law',
                early_escape_model=early_escape_model
            ))
        elif element == 'econ':
            validators.append(ModelValidator(
                model_validator_model,
                f"We are analyzing economic activity in a German tax case. Does this deduction in any way prove or help to prove applicable law (treaties, statutes) or procedural requirements (filing, documentation) given the case description below?\n\n{description}",
                "We are proving economic activity only. We do not want to prove applicable law or procedural requirements because that could make the reasoning complicated.",
                conditional='Economic activity',
                early_escape_model=early_escape_model
            ))
        elif element == 'proc':
            validators.append(ModelValidator(
                model_validator_model,
                f"We are analyzing procedural requirements in a German tax case. Does this deduction in any way prove or help to prove applicable law (treaties, statutes) or economic activity (revenue, business operations) given the case description below?\n\n{description}",
                "We are proving procedural requirements only. We do not want to prove applicable law or economic activity because that could make the reasoning complicated.",
                conditional='Procedural requirements',
                early_escape_model=early_escape_model
            ))
    
    return validators


def expand_node_with_crew(
    agent: Agent,
    tree: LogicTree,
    node: LogicNode,
    description: str,
    case: dict = None,
    max_retries: int = 3,
    use_model_validator: bool = False,
    model_validator_model: OpenAIModel = None,
    early_escape_model: OpenAIModel = None
) -> List[str]:
    """
    Use CrewAI to generate child lines for the given node with validation.
    
    Args:
        agent: The tree expansion agent
        tree: Current logic tree state
        node: Node to expand
        description: Case description
        case: Case metadata for validators
        max_retries: Maximum number of retry attempts
        use_model_validator: Whether to use LLM-based validation (expensive)
        model_validator_model: Main model for LLM validation
        early_escape_model: Cheaper model for initial validation
        
    Returns:
        List of child line strings in format: "text | Fact From Story" or "text | Commonsense Knowledge"
    """
    depth = get_node_depth(node)
    element_key = get_node_element(node)
    
    # Determine level key
    if depth == 1:
        level_key = 'l1_l2'
    elif depth == 2:
        level_key = 'l2_l3'
    else:
        return []  # No expansion beyond depth 2
    
    asset_key = f"{element_key}_{level_key}"
    
    if asset_key not in _PROMPTS_ASSET:
        # No specific asset for this combination, skip
        return []
    
    asset = _PROMPTS_ASSET[asset_key]
    guideline = asset.get('guideline', '')
    example = asset.get('example', {})
    
    # Build task description with examples first, then current state
    task_description = f"""
**Level and Element-specific Guidelines:**
{guideline}

**Example Description (for reference):**
{join_lines(example.get('description', []))}

**Example Tree (for reference):**
{join_lines(example.get('example_tree', []))}

**Example Node Completion (content reference):**
{join_lines(example.get('example_node_completion', []))}

---

**YOUR TURN:**

**Current Case Description:**
{description}

**Current Tree State:**
{render_tree_state(tree)}

**Node to Expand:**
{node.value if node.value else "[ERROR: Node value is empty]"}

**Your Task:**
Generate exactly 3 child lines for the node "{node.value if node.value else 'EMPTY NODE'}":
- 2 lines ending with "| Fact From Story"
- 1 line ending with "| Commonsense Knowledge"

Output ONLY the 3 child lines in the following format (one per line):
> <fact text> | Fact From Story
> <fact text> | Fact From Story
> <fact text> | Commonsense Knowledge

Do NOT include any other text, explanations, or markdown. Just the 3 lines.
""".strip()

    # Create validators
    validators = create_validators(
        node, 
        case or {}, 
        use_model_validator=use_model_validator,
        model_validator_model=model_validator_model,
        early_escape_model=early_escape_model
    )
    
    # Retry loop with validation
    for retry_attempt in range(max_retries + 1):
        task = Task(
            description=task_description,
            agent=agent,
            expected_output="Exactly 3 child node lines in the specified format"
        )
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        
        # Parse result
        output = str(result).strip()
        lines = [line.strip() for line in output.split('\n') if line.strip() and '|' in line]
        
        # Clean up lines (remove leading '>')
        cleaned_lines = []
        for line in lines:
            line = line.lstrip('> ').strip()
            if '|' in line:
                cleaned_lines.append(line)
        
        # Parse into explicit and commonsense facts
        explicit_facts = []
        commonsense_facts = []
        
        for line in cleaned_lines[:3]:
            if '| Commonsense Knowledge' in line:
                text = line.split('|')[0].strip()
                commonsense_facts.append(text)
            elif '| Fact From Story' in line or '| Complex Fact' in line:
                text = line.split('|')[0].strip()
                explicit_facts.append(text)
        
        # Run validators (node.children already has fact_type set by build_structure)
        all_valid = True
        for validator in validators:
            valid, retry_prompt = validator(node, explicit_facts, commonsense_facts, output)
            if not valid:
                print(f"Validation failed (attempt {retry_attempt + 1}/{max_retries + 1})")
                print(f"Retry reason: {retry_prompt}")
                
                # Append retry prompt to task description
                task_description += f"\n\n{retry_prompt}"
                all_valid = False
                break
        
        if all_valid:
            return cleaned_lines[:3]
    
    # If all retries failed, return empty (will kill branch)
    print(f"All validation attempts failed for node: {node.value}")
    return []

