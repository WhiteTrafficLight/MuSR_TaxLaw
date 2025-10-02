"""
Economic (Economic Activity) expansion prompts for German tax case tree generation.
"""

ECON_L1_L2_GUIDELINE = """
Economic L1→L2 expansion: qualitative-only; forbid numbers, percentages, currencies, and years. 
Generate exactly 2 Explicit + 1 Commonsense. Each Explicit ≤ 25 words, may be framed as a Complex Fact 
to allow level-3 decomposition. Focus on dependence on parent relationships vs. independent market 
development using generic phrasing.
""".strip()

ECON_L1_L2_EXAMPLE_DESCRIPTION = [
    "Taxpayer: TechnoGmbH",
    "Business sector: IT consulting and software development",
    "Transaction type: ip_licensing",
    "Applicable law: Article 12 OECD Model Tax Convention (royalty taxation)",
    "Economic activity: Revenue growth predominantly from existing parent company licensee relationships",
    "Procedural requirement: Transfer pricing documentation with royalty rate benchmarking submitted timely",
    "Tax authority: Finanzamt München"
]

ECON_L1_L2_EXAMPLE_TREE = [
    "Finanzamt München should accept with conditions the arrangement by TechnoGmbH. | Deduced Root Conclusion",
    "> Applicable law is clear for TechnoGmbH's arrangement. | Deduced Fact",
    "> Economic activity is insufficient for TechnoGmbH's operations. | Deduced Fact",
    "> Procedural requirements are compliant for TechnoGmbH's arrangement. | Deduced Fact"
]

ECON_L1_L2_EXAMPLE_NODE_COMPLETION = [
    "> Economic activity is insufficient for TechnoGmbH's operations.",
    "> > A substantial portion of new engagements originated from entities with prior ties to the parent. | Fact From Story",
    "> > New market development by the subsidiary remained limited relative to inherited channels. | Fact From Story",
    "> > When expansion relies primarily on preexisting relationships rather than independent acquisition, economic substance is constrained. | Commonsense Knowledge"
]

ECON_L1_L2 = {
    "guideline": ECON_L1_L2_GUIDELINE,
    "example": {
        "description": ECON_L1_L2_EXAMPLE_DESCRIPTION,
        "example_tree": ECON_L1_L2_EXAMPLE_TREE,
        "example_node_completion": ECON_L1_L2_EXAMPLE_NODE_COMPLETION,
    }
}


ECON_L2_L3_GUIDELINE = """
Economic L2→L3 expansion: operationalize prior qualitative facts by introducing concrete metrics 
(counts, amounts, dates) and document specifics. Break each Complex Fact into 2-3 atomic Fact From Story 
items plus 1 Commonsense that connects them to the parent deduction. Maintain element purity (economic only).
""".strip()

ECON_L2_L3_EXAMPLE_DESCRIPTION = [
    "Taxpayer: TechnoGmbH",
    "Business sector: IT consulting and software development",
    "Transaction type: ip_licensing",
    "Applicable law: Article 12 OECD Model Tax Convention (royalty taxation)",
    "Economic activity: Revenue growth predominantly from existing parent company licensee relationships",
    "Procedural requirement: Transfer pricing documentation with royalty rate benchmarking submitted timely",
    "Tax authority: Finanzamt München"
]

ECON_L2_L3_EXAMPLE_TREE = [
    "Finanzamt München should accept with conditions the arrangement by TechnoGmbH. | Deduced Root Conclusion",
    "> Applicable law is clear for TechnoGmbH's arrangement. | Deduced Fact",
    "> > TechnoGmbH's arrangement involves cross-border licensing with periodic payments for intellectual property rights. | Fact From Story",
    "> > The transaction structure aligns with established international frameworks for royalty taxation. | Fact From Story",
    "> > When licensing agreements involve periodic payments for IP exploitation, relevant international tax provisions provide clear legal classification. | Commonsense Knowledge",
    "> Economic activity is insufficient for TechnoGmbH's operations. | Deduced Fact",
    "> > A substantial portion of new engagements originated from entities with prior ties to the parent. | Fact From Story",
    "> > New market development by the subsidiary remained limited relative to inherited channels. | Fact From Story",
    "> > When expansion relies primarily on preexisting relationships rather than independent acquisition, economic substance is constrained. | Commonsense Knowledge",
    "> Procedural requirements are compliant for TechnoGmbH's arrangement. | Deduced Fact",
    "> > Transfer pricing documentation includes a benchmarking analysis of royalty rates. | Fact From Story",
    "> > The documentation was submitted within the prescribed statutory timeframe. | Fact From Story",
    "> > When required analyses are included and filing is timely, procedural compliance is satisfied. | Commonsense Knowledge"
]

ECON_L2_L3_EXAMPLE_NODE_COMPLETION = [
    "> > A substantial portion of new engagements originated from entities with prior ties to the parent.",
    "> > > 58.3% of new contracts signed in FY2024 were with entities previously covered under parent company agreements. | Fact From Story",
    "> > > Independent client acquisition efforts yielded 12 net-new customers during the 2024 fiscal year, per internal sales logs. | Fact From Story",
    "> > > When the majority of new business stems from preexisting parent relationships and independent prospecting remains minimal, reliance on inherited channels is demonstrated. | Commonsense Knowledge"
]

ECON_L2_L3 = {
    "guideline": ECON_L2_L3_GUIDELINE,
    "example": {
        "description": ECON_L2_L3_EXAMPLE_DESCRIPTION,
        "example_tree": ECON_L2_L3_EXAMPLE_TREE,
        "example_node_completion": ECON_L2_L3_EXAMPLE_NODE_COMPLETION,
    }
}

