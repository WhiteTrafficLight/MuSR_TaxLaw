"""
Main orchestration for German tax case generation using CrewAI.
"""

import json
import random
from typing import List

from crewai import Task, Crew

from src import cache
from src.model.openai import OpenAIModel
from src.utils.paths import OUTPUT_FOLDER, ROOT_FOLDER
from src.dataset_types.german_tax_dataset import GermanTaxDataset

from src.crews.agents import create_tree_agent, create_story_agent
from src.crews.scenario import sample_scenario, build_case_variants
from src.crews.tree_builder import make_root_tree, expand_tree_with_crew
from src.crews.html_renderer import generate_html_page_comparison
from src.crews.config.prompts.story import STORY_GENERATION_PROMPT



def run_single_german_tax_case(use_model_validator: bool = False):
    """
    Generate a single German tax case with reasoning tree and story using CrewAI.
    Outputs JSON dataset and HTML visualization.
    
    Args:
        use_model_validator: Whether to use LLM-based validation (more accurate but expensive)
    """
    # Setup cache
    cache.enable()
    if hasattr(cache, 'redis_backend') and cache.redis_backend:
        cache.redis_backend.flushdb()

    # Setup output paths
    out_file = OUTPUT_FOLDER / 'german_tax_law_case.json'
    out_file.parent.mkdir(exist_ok=True, parents=True)
    html_file = ROOT_FOLDER / 'german_tax_law_case.html'

    # Initialize models
    model = OpenAIModel(
        engine='gpt-4',
        api_max_attempts=30,
        api_endpoint='chat',
        temperature=1.0,
        top_p=1.0,
        max_tokens=2400,
        num_samples=1,
        prompt_cost=0.03/1000,
        completion_cost=0.06/1000
    )
    
    # Optional: model for validation (if enabled)
    model_validator_model = None
    early_escape_model = None
    if use_model_validator:
        model_validator_model = OpenAIModel(
            engine='gpt-4',
            api_max_attempts=30,
            api_endpoint='chat',
            temperature=0.0,  # Use deterministic for validation
            max_tokens=500,
            num_samples=1,
            prompt_cost=0.03/1000,
            completion_cost=0.06/1000
        )
        early_escape_model = OpenAIModel(
            engine='gpt-3.5-turbo',
            api_max_attempts=30,
            api_endpoint='chat',
            temperature=0.0,
            max_tokens=500,
            num_samples=1,
            prompt_cost=0.0015/1000,
            completion_cost=0.002/1000
        )
    
    creator = GermanTaxDataset()

    # Create agents
    tree_agent = create_tree_agent(model="gpt-4", temperature=1.0)
    story_agent = create_story_agent(model="gpt-4", temperature=1.0)

    # Sample scenario and build two contrasting cases
    scenario_info, scenario_header, base_madlib, tx_madlib, tx_type = sample_scenario()
    business_sector = scenario_info.get('business_sector', 'N/A')
    cases = build_case_variants(base_madlib, tx_madlib, business_sector, tx_type)  # Returns 2 cases

    # Process both cases
    case_data = []
    for idx, case in enumerate(cases):
        taxpayer = case['taxpayer']
        base_tree = make_root_tree({**case, 'taxpayer': taxpayer})
        
        full_tree = expand_tree_with_crew(
            tree_agent, 
            creator, 
            case, 
            base_tree,
            use_model_validator=use_model_validator,
            model_validator_model=model_validator_model,
            early_escape_model=early_escape_model
        )
        
        case_tree = {
            'tree': full_tree,
            'description': case['description'],
            'case_info': case,
            'scenario_info': scenario_info
        }

        # Extract correct tree (filters to 3 elements: law, econ, proc)
        case_trees = creator.create_chapter_trees([case_tree])
        chosen = case_trees[0]
        correct_tree = chosen['correct_tree']

        # Extract L2->L3 facts from the tree (leaf Fact From Story nodes)
        facts = [x.value for x in correct_tree.get_facts()]
        
        case_data.append({
            'case_num': idx + 1,
            'case_info': case,
            'correct_tree': correct_tree,
            'facts': facts
        })
    
    # Generate stories for both cases
    example = STORY_GENERATION_PROMPT
    example_case_str = "\n".join(example['example_case_info'])
    example_facts_str = "\n".join([f'- {f}' for f in example['example_facts']])
    example_output = example['example_output']
    
    stories = []
    for data in case_data:
        case = data['case_info']
        facts = data['facts']
        facts_str = "\n".join([f'- {x}' for x in facts])
        
        # Format case info
        applicable_law_str = case['applicable_law'] if isinstance(case['applicable_law'], str) else case['applicable_law'][0]
        economic_activity_str = case['economic_activity'] if isinstance(case['economic_activity'], str) else case['economic_activity'][0]
        procedural_requirement_str = case['procedural_requirement'] if isinstance(case['procedural_requirement'], str) else case['procedural_requirement'][0]
        tax_authority_str = case['tax_authority'] if isinstance(case['tax_authority'], str) else case['tax_authority'][0]
        
        case_info_str = f"""Taxpayer: {case['taxpayer']}
Business sector: {business_sector}
Transaction type: {tx_type}
Applicable law: {applicable_law_str}
Economic activity: {economic_activity_str}
Procedural requirement: {procedural_requirement_str}
Tax authority: {tax_authority_str}"""
        
        # Create story generation task
        story_task_description = f"""
Write a formal German tax court decision section that presents the case facts objectively.

**Example Case Information:**
{example_case_str}

**Example Facts to Include:**
{example_facts_str}

**Example Output:**
{example_output}

---

**Your Turn:**

**Case Information:**
{case_info_str}

**Facts you must include:**
{facts_str}

**Your Task:**
Write a formal court decision section that:
1. Presents all the facts listed above in formal court language
2. Uses third person and passive voice
3. Integrates facts naturally without explicit section headings
4. Maintains professional neutrality and legal precision throughout
5. Focuses purely on factual presentation without drawing conclusions

**CRITICAL CONSTRAINTS:**
This text will be used for logical reasoning exercises where readers must infer the final decision themselves. Therefore:
- Do NOT hint at whether applicable law is "clear" or "unclear"
- Do NOT hint at whether economic activity is "sufficient" or "insufficient"  
- Do NOT hint at whether procedural requirements are "compliant" or "deficient"
- Do NOT hint at the final decision (accept/accept with conditions/reject)
- Include all factual content from the list above, but remove or rephrase any expressions that obviously suggest element status or final judgment
- Present facts neutrally so readers must perform logical inference to reach conclusions

Write only the factual content, without title, case number, or concluding remarks.
""".strip()
        
        story_task = Task(
            description=story_task_description,
            agent=story_agent,
            expected_output="A formal court decision section presenting all facts objectively"
        )
        
        story_crew = Crew(
            agents=[story_agent],
            tasks=[story_task],
            verbose=True
        )
        
        story_result = story_crew.kickoff()
        stories.append(str(story_result).strip())

    # Combine stories for comparison
    combined_context = f"""Following are two different tax law cases for similar transaction type.

Case 1:
{stories[0]}

Case 2:
{stories[1]}"""

    # Build choices for comparison question
    # Case 1 is "accept with conditions" (2 elements satisfied)
    # Case 2 is "fully reject" (1 element satisfied)
    # Therefore Case 1 is more likely to be accepted
    choices = ["Case 1", "Case 2"]
    labeled = [f"A) {choices[0]}", f"B) {choices[1]}"]

    # Create dataset item with both trees
    tree_jsons = [data['correct_tree'].to_json() for data in case_data]
    dataset_item = {
        'context': combined_context,
        'questions': [{
            'question': 'Which case is more likely to be accepted?',
            'choices': labeled,
            'answer': 0,  # Case 1 (accept with conditions) is more likely than Case 2 (fully reject)
            'intermediate_trees': [tree_jsons],
            'intermediate_data': [[{
                'case_info': data['case_info'],
                'scenario_info': scenario_info,
            } for data in case_data]]
        }]
    }

    # Write JSON output
    out_file.write_text(
        json.dumps([dataset_item], ensure_ascii=False), 
        encoding='utf-8'
    )

    # Generate and write HTML (show both trees and both stories)
    html_content = generate_html_page_comparison(case_data, stories, labeled, business_sector, tx_type)
    html_file.write_text(html_content, encoding='utf-8')

    # Print cost summary
    total_cost = model.total_cost
    if use_model_validator and model_validator_model:
        total_cost += model_validator_model.total_cost
        if early_escape_model:
            total_cost += early_escape_model.total_cost
    
    print('✅ Wrote dataset to', str(out_file))
    print('✅ Wrote HTML to', str(html_file))
    print(f'💰 Total cost: ${total_cost:.4f}')

