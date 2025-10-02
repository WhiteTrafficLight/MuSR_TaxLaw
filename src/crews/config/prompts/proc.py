"""
Procedural (Procedural Requirements) expansion prompts for German tax case tree generation.
"""

PROC_L1_L2_GUIDELINE = """
Procedural L1→L2 expansion: qualitative-only; forbid numbers/dates/specific page counts. 
Generate exactly 2 Explicit + 1 Commonsense. Each Explicit ≤ 25 words and may be framed as a Complex Fact 
to allow further breakdown at next level. Emphasize that required analyses are present and filing was within 
the prescribed timeframe using generic phrasing.
""".strip()

PROC_L1_L2_EXAMPLE_DESCRIPTION = [
    "Taxpayer: TechnoGmbH",
    "Business sector: IT consulting and software development",
    "Transaction type: ip_licensing",
    "Applicable law: Article 12 OECD Model Tax Convention (royalty taxation)",
    "Economic activity: Revenue growth predominantly from existing parent company licensee relationships",
    "Procedural requirement: Transfer pricing documentation with royalty rate benchmarking submitted timely",
    "Tax authority: Finanzamt München"
]

PROC_L1_L2_EXAMPLE_TREE = [
    "Finanzamt München should accept with conditions the arrangement by TechnoGmbH. | Deduced Root Conclusion",
    "> Applicable law is clear for TechnoGmbH's arrangement. | Deduced Fact",
    "> > TechnoGmbH's arrangement involves cross-border licensing with periodic payments for intellectual property rights. | Fact From Story",
    "> > The transaction structure aligns with established international frameworks for royalty taxation. | Fact From Story",
    "> > When licensing agreements involve periodic payments for IP exploitation, relevant international tax provisions provide clear legal classification. | Commonsense Knowledge",
    "> Economic activity is insufficient for TechnoGmbH's operations. | Deduced Fact",
    "> > A substantial portion of new engagements originated from entities with prior ties to the parent. | Fact From Story",
    "> > New market development by the subsidiary remained limited relative to inherited channels. | Fact From Story",
    "> > When expansion relies primarily on preexisting relationships rather than independent acquisition, economic substance is constrained. | Commonsense Knowledge",
    "> Procedural requirements are compliant for TechnoGmbH's arrangement. | Deduced Fact"
]

PROC_L1_L2_EXAMPLE_NODE_COMPLETION = [
    "> Procedural requirements are compliant for TechnoGmbH's arrangement.",
    "> > Transfer pricing documentation includes a benchmarking analysis of royalty rates. | Fact From Story",
    "> > The documentation was submitted within the prescribed statutory timeframe. | Fact From Story",
    "> > When required analyses are included and filing is timely, procedural compliance is satisfied. | Commonsense Knowledge"
]

PROC_L1_L2 = {
    "guideline": PROC_L1_L2_GUIDELINE,
    "example": {
        "description": PROC_L1_L2_EXAMPLE_DESCRIPTION,
        "example_tree": PROC_L1_L2_EXAMPLE_TREE,
        "example_node_completion": PROC_L1_L2_EXAMPLE_NODE_COMPLETION,
    }
}


PROC_L2_L3_GUIDELINE = """
Procedural L2→L3 expansion: introduce specific filing timestamps, document sections, or required annexes 
to operationalize prior qualitative compliance statements. Split into atomic facts and one commonsense 
linking timely/complete submission to compliance.
""".strip()

PROC_L2_L3_EXAMPLE_DESCRIPTION = [
    "Taxpayer: TechnoGmbH",
    "Business sector: IT consulting and software development",
    "Transaction type: ip_licensing",
    "Applicable law: Article 12 OECD Model Tax Convention (royalty taxation)",
    "Economic activity: Revenue growth predominantly from existing parent company licensee relationships",
    "Procedural requirement: Transfer pricing documentation with royalty rate benchmarking submitted timely",
    "Tax authority: Finanzamt München"
]

PROC_L2_L3_EXAMPLE_TREE = [
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

PROC_L2_L3_EXAMPLE_NODE_COMPLETION = [
    "> > Transfer pricing documentation includes a benchmarking analysis of royalty rates.",
    "> > > The documentation totaling 350 pages was submitted via ELSTER electronic filing system. | Fact From Story",
    "> > > The benchmarking analysis section references 12 comparable transactions per Annex B requirements. | Fact From Story",
    "> > > When transfer pricing documentation includes required comparable analysis sections and is filed electronically within prescribed format, benchmarking compliance is achieved. | Commonsense Knowledge"
]

PROC_L2_L3 = {
    "guideline": PROC_L2_L3_GUIDELINE,
    "example": {
        "description": PROC_L2_L3_EXAMPLE_DESCRIPTION,
        "example_tree": PROC_L2_L3_EXAMPLE_TREE,
        "example_node_completion": PROC_L2_L3_EXAMPLE_NODE_COMPLETION,
    }
}

