"""
Story generation prompt and example for German tax court document writing.
"""

STORY_GENERATION_EXAMPLE_CASE_INFO = [
    "Taxpayer: TechnoGmbH",
    "Business sector: IT consulting and software development",
    "Transaction type: ip_licensing",
    "Applicable law: Article 12 OECD Model Tax Convention (royalty taxation)",
    "Economic activity: Revenue growth predominantly from existing parent company licensee relationships",
    "Procedural requirement: Transfer pricing documentation with royalty rate benchmarking submitted timely",
    "Tax authority: Finanzamt München",
]

STORY_GENERATION_EXAMPLE_FACTS = [
    "The licensing agreement grants software usage rights between Germany and Netherlands-based related entities.",
    "Payments are structured as royalties for IP exploitation under the terms of the bilateral treaty.",
    "The contractual documentation labels payments as 'royalties for software usage rights' per clause 4.2.",
    "Germany and Netherlands maintain a bilateral tax treaty based on the OECD Model Tax Convention framework.",
    "58% of new contracts signed in FY2024 were with entities previously covered under parent company agreements.",
    "Independent client acquisition efforts yielded 12 net-new customers during the 2024 fiscal year, per internal sales logs.",
    "Marketing expenditures allocated to new customer segments totaled €47,000 in FY2024, representing 8% of total marketing budget.",
    "Geographic expansion initiatives resulted in operational presence in 2 additional cities during the reporting period, per quarterly business reports.",
    "The documentation totaling 350 pages was submitted via ELSTER electronic filing system.",
    "The benchmarking analysis section references 12 comparable transactions per Annex B requirements."
]

STORY_GENERATION_EXAMPLE_OUTPUT = """
It was established that TechnoGmbH entered into a licensing arrangement concerning software usage rights. The agreement was executed between entities based in Germany and the Netherlands, with both parties being related entities within the same corporate group. Upon examination of the contractual terms, it was determined that payments under the agreement are structured as royalties for the exploitation of intellectual property rights.

The contractual documentation submitted for review labels these payments as 'royalties for software usage rights' per clause 4.2 of the agreement. The records show that Germany and Netherlands maintain a bilateral tax treaty based on the OECD Model Tax Convention framework, under which such payments are governed by the applicable international tax provisions.

The financial records reveal that during fiscal year 2024, TechnoGmbH entered into multiple new licensing contracts. Analysis of these contracts shows that 58% of newly executed agreements were with entities that had previously been serviced under parent company arrangements. Internal sales documentation indicates that independent client acquisition initiatives resulted in 12 net-new customer relationships during the 2024 fiscal year, as verified through examination of the company's sales logs and customer relationship management records.

Upon review of the marketing budget allocations, it was found that expenditures directed toward new customer segments amounted to €47,000 during fiscal year 2024, representing 8% of the total marketing budget for the reporting period. The quarterly business reports document that geographic expansion activities resulted in the establishment of operational presence in 2 additional cities during the relevant period.

The transfer pricing documentation submitted by TechnoGmbH comprises 350 pages and was transmitted via the ELSTER electronic filing system, as evidenced by the system timestamp. The benchmarking analysis section of the documentation contains references to 12 comparable transactions, which are detailed in Annex B of the submission in accordance with the prescribed requirements for transfer pricing documentation.
""".strip()

STORY_GENERATION_PROMPT = {
    "example_case_info": STORY_GENERATION_EXAMPLE_CASE_INFO,
    "example_facts": STORY_GENERATION_EXAMPLE_FACTS,
    "example_output": STORY_GENERATION_EXAMPLE_OUTPUT
}

COURT_DECISION_TASK_TEMPLATE = """
**Example Case Information:**
{example_case_str}

**Example Facts to Include:**
{example_facts_str}

**Example Output:**
{example_output}

---

**Your Task:**

**Case Information:**
{case_info_str}

**Facts you must include:**
{facts_str}

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

