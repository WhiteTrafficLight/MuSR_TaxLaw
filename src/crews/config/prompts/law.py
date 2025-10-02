"""
Law (Applicable Law) expansion prompts for German tax case tree generation.
"""

LAW_L1_L2_GUIDELINE = """
Law L1→L2 expansion: describe transaction's legal characteristics that relate to the 'Applicable law' 
stated in case description, but without citing specific treaty articles or statute numbers yet. 
Generate exactly 2 Explicit + 1 Commonsense. Each Explicit ≤ 30 words describing transaction type 
(e.g. 'cross-border licensing', 'periodic payments', 'IP rights'). Commonsense references general 
treaty/statute frameworks WITHOUT specific article numbers. Frame as Complex Facts for L3 decomposition.
""".strip()

LAW_L1_L2_EXAMPLE_DESCRIPTION = [
    "Taxpayer: TechnoGmbH",
    "Business sector: IT consulting and software development",
    "Transaction type: ip_licensing",
    "Applicable law: Article 12 OECD Model Tax Convention (royalty taxation)",
    "Economic activity: Revenue growth predominantly from existing parent company licensee relationships",
    "Procedural requirement: Transfer pricing documentation with royalty rate benchmarking submitted timely",
    "Tax authority: Finanzamt München"
]

LAW_L1_L2_EXAMPLE_TREE = [
    "Finanzamt München should accept with conditions the arrangement by TechnoGmbH. | Deduced Root Conclusion",
    "> Applicable law is clear for TechnoGmbH's arrangement. | Deduced Fact",
    "> Economic activity is insufficient for TechnoGmbH's operations. | Deduced Fact",
    "> Procedural requirements are compliant for TechnoGmbH's arrangement. | Deduced Fact"
]

LAW_L1_L2_EXAMPLE_NODE_COMPLETION = [
    "> Applicable law is clear for TechnoGmbH's arrangement.",
    "> > TechnoGmbH's arrangement involves cross-border licensing with periodic payments for intellectual property rights. | Fact From Story",
    "> > The transaction structure aligns with established international frameworks for royalty taxation. | Fact From Story",
    "> > When licensing agreements involve periodic payments for IP exploitation, relevant international tax provisions provide clear legal classification. | Commonsense Knowledge"
]

LAW_L1_L2 = {
    "guideline": LAW_L1_L2_GUIDELINE,
    "example": {
        "description": LAW_L1_L2_EXAMPLE_DESCRIPTION,
        "example_tree": LAW_L1_L2_EXAMPLE_TREE,
        "example_node_completion": LAW_L1_L2_EXAMPLE_NODE_COMPLETION,
    }
}


LAW_L2_L3_GUIDELINE = """
Law L2→L3 expansion: decompose L2 legal characteristics into specific treaty/statutory elements from 
the case description's 'Applicable law' field. ONLY use the legal provision already stated in the case 
description - do not invent new treaties or statutes. Generate 2 Explicit describing transaction conditions 
+ 1 Commonsense citing the EXACT provision from case description. Focus on jurisdictional elements, 
transaction structure, and legal definitions.
""".strip()

LAW_L2_L3_EXAMPLE_DESCRIPTION = [
    "Taxpayer: TechnoGmbH",
    "Business sector: IT consulting and software development",
    "Transaction type: ip_licensing",
    "Applicable law: Article 12 OECD Model Tax Convention (royalty taxation)",
    "Economic activity: Revenue growth predominantly from existing parent company licensee relationships",
    "Procedural requirement: Transfer pricing documentation with royalty rate benchmarking submitted timely",
    "Tax authority: Finanzamt München"
]

LAW_L2_L3_EXAMPLE_TREE = [
    "Finanzamt München should accept with conditions the arrangement by TechnoGmbH. | Deduced Root Conclusion",
    "> Applicable law is clear for TechnoGmbH's arrangement. | Deduced Fact",
    "> > TechnoGmbH's arrangement involves cross-border licensing with periodic payments for intellectual property rights. | Fact From Story",
    "> > > The licensing agreement grants software usage rights between Germany and Netherlands-based related entities. | Fact From Story",
    "> > > Payments are structured as royalties for IP exploitation under the terms of the bilateral treaty. | Fact From Story",
    "> > > When cross-border IP licensing between treaty partners involves royalty payments for software rights, Article 12 OECD Model Tax Convention provides the governing legal framework. | Commonsense Knowledge",
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

LAW_L2_L3_EXAMPLE_NODE_COMPLETION = [
    "> > The transaction structure aligns with established international frameworks for royalty taxation.",
    "> > > The contractual documentation labels payments as 'royalties for software usage rights' per clause 4.2. | Fact From Story",
    "> > > Germany and Netherlands maintain a bilateral tax treaty based on the OECD Model Tax Convention framework. | Fact From Story",
    "> > > When cross-border payments are contractually labeled as royalties between OECD Model Convention treaty partners, the bilateral framework provides applicable taxation provisions. | Commonsense Knowledge"
]

LAW_L2_L3 = {
    "guideline": LAW_L2_L3_GUIDELINE,
    "example": {
        "description": LAW_L2_L3_EXAMPLE_DESCRIPTION,
        "example_tree": LAW_L2_L3_EXAMPLE_TREE,
        "example_node_completion": LAW_L2_L3_EXAMPLE_NODE_COMPLETION,
    }
}

