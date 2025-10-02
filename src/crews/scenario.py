"""
Scenario sampling and case variant building for German tax cases.
"""

import json
import random
from typing import Dict, List, Tuple

from src.madlib.madlib import Madlib
from src.utils.paths import ROOT_FOLDER


def sample_scenario() -> Tuple[Dict, str, Madlib, Madlib, str]:
    """
    Sample a base scenario (taxpayer, business sector, transaction type).
    
    Returns:
        Tuple of (scenario_info, scenario_header, base_madlib, tx_madlib, tx_type)
    """
    from src.dataset_types.german_tax_dataset import GermanTaxDataset
    
    creator = GermanTaxDataset()
    base_madlib = Madlib(
        {
            "taxpayer_types": ROOT_FOLDER / 'domain_seed/taxpayer_types.json',
            "business_sectors": ROOT_FOLDER / 'domain_seed/business_sectors.json',
            "tax_authorities": ROOT_FOLDER / 'domain_seed/tax_authorities.json',
        }
    )

    description_string = """Taxpayer: {taxpayer}
Business sector: {business_sector}"""

    case_strings, case_dicts, _ = creator.sample_madlib(
        base_madlib,
        ['taxpayer_types', 'business_sectors'],
        description_string_format=description_string,
        sampled_item_names=['taxpayer', 'business_sector']
    )

    scenario_info = case_dicts[0]
    business_sector = scenario_info['business_sector']

    # Select transaction type based on business sector
    tx_types_map_path = ROOT_FOLDER / 'domain_seed/transaction_types_map.json'
    tx_types_map = json.loads(tx_types_map_path.read_text(encoding='utf-8'))
    available_tx = tx_types_map['sector_to_transactions'].get(
        business_sector, 
        ['ip_licensing', 'function_transfer']
    )
    tx_type = random.choice(available_tx)

    # Load transaction-specific madlib
    tx_domain_path = ROOT_FOLDER / f'domain_seed/{tx_type}'
    tx_madlib = Madlib(
        {
            "applicable_laws_clear": tx_domain_path / 'applicable_laws_clear.json',
            "economic_activities_sufficient": tx_domain_path / 'economic_activities_sufficient.json',
            "procedural_requirements_compliant": tx_domain_path / 'procedural_requirements_compliant.json',
            "applicable_laws_unclear": tx_domain_path / 'applicable_laws_unclear.json',
            "economic_activities_insufficient": tx_domain_path / 'economic_activities_insufficient.json',
            "procedural_requirements_deficient": tx_domain_path / 'procedural_requirements_deficient.json',
        }
    )

    return scenario_info, case_strings[0], base_madlib, tx_madlib, tx_type


def build_case_variants(
    base_madlib: Madlib, 
    tx_madlib: Madlib, 
    business_sector: str,
    tx_type: str
) -> List[Dict]:
    """
    Build two contrasting cases for comparison reasoning:
    - Case 1: 2 elements satisfied → accept with conditions
    - Case 2: 1 element satisfied → fully reject
    
    Both cases share same business sector and transaction type, but have different
    taxpayers and tax authorities to create a realistic comparison scenario.
    
    Args:
        base_madlib: Base madlib for common elements
        tx_madlib: Transaction-specific madlib
        business_sector: Business sector (shared between cases)
        tx_type: Transaction type (shared between cases)
        
    Returns:
        List with two case dictionaries for comparison
    """
    # Sample two different taxpayers and tax authorities
    taxpayer1 = base_madlib.sample("taxpayer_types")
    taxpayer2 = base_madlib.sample("taxpayer_types")
    while taxpayer2 == taxpayer1:
        taxpayer2 = base_madlib.sample("taxpayer_types")
    
    tax_authority1 = base_madlib.sample("tax_authorities")
    tax_authority2 = base_madlib.sample("tax_authorities")
    while tax_authority2 == tax_authority1:
        tax_authority2 = base_madlib.sample("tax_authorities")
    
    # Case 1: Accept with conditions (2 elements satisfied, 1 deficient)
    # Randomly choose which element is deficient
    accept_conditions_patterns = [
        ("clear", "sufficient", "deficient"),      # Procedural deficiency
        ("clear", "insufficient", "compliant"),    # Economic deficiency
        ("unclear", "sufficient", "compliant"),    # Legal ambiguity
    ]
    law1, econ1, proc1 = random.choice(accept_conditions_patterns)
    
    # Case 2: Fully reject (1 element satisfied, 2 deficient)
    # Must be worse than case 1
    reject_patterns = [
        ("unclear", "insufficient", "compliant"),  # Law unclear + econ deficient
        ("unclear", "insufficient", "deficient"),  # Law unclear + econ + proc deficient
        ("unclear", "sufficient", "deficient"),    # Law unclear + proc deficient
        ("clear", "insufficient", "deficient"),    # Econ + proc deficient
    ]
    law2, econ2, proc2 = random.choice(reject_patterns)
    
    # Build case 1
    case1 = {
        'final_decision': 'accept with conditions',
        'taxpayer': taxpayer1,
        'tax_authority': tax_authority1,
        'business_sector': business_sector,
        'transaction_type': tx_type,
        'law_state': law1,
        'econ_state': econ1,
        'proc_state': proc1,
        'applicable_law': tx_madlib.sample(f"applicable_laws_{law1}"),
        'economic_activity': tx_madlib.sample(f"economic_activities_{econ1}"),
        'procedural_requirement': tx_madlib.sample(f"procedural_requirements_{proc1}"),
    }
    
    case1['description'] = f"""Taxpayer: {taxpayer1}
Business sector: {business_sector}
Transaction type: {tx_type}
Applicable law: {case1['applicable_law']}
Economic activity: {case1['economic_activity']}
Procedural requirement: {case1['procedural_requirement']}
Tax authority: {tax_authority1}""".strip()
    
    # Build case 2
    case2 = {
        'final_decision': 'fully reject',
        'taxpayer': taxpayer2,
        'tax_authority': tax_authority2,
        'business_sector': business_sector,
        'transaction_type': tx_type,
        'law_state': law2,
        'econ_state': econ2,
        'proc_state': proc2,
        'applicable_law': tx_madlib.sample(f"applicable_laws_{law2}"),
        'economic_activity': tx_madlib.sample(f"economic_activities_{econ2}"),
        'procedural_requirement': tx_madlib.sample(f"procedural_requirements_{proc2}"),
    }
    
    case2['description'] = f"""Taxpayer: {taxpayer2}
Business sector: {business_sector}
Transaction type: {tx_type}
Applicable law: {case2['applicable_law']}
Economic activity: {case2['economic_activity']}
Procedural requirement: {case2['procedural_requirement']}
Tax authority: {tax_authority2}""".strip()
    
    return [case1, case2]

