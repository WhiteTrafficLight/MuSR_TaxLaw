"""
Example of solving a German Tax Case comparison with step-by-step reasoning.
Based on actual generated cases from the dataset.
"""

story = """
Following are two different tax law cases for similar transaction type.

Case 1:
It was established that TechStart Innovation UG undertook a transfer of certain functions, comprising the management of power grid connectivity, optimizing energy efficiency, and integrating renewable energy sources. As part of this transfer, the operation of these functions was directed from Germany to multiple foreign entities.

Upon examination of the operational setup, it was revealed that the company maintains a customer service hub, staffed by thirty full-time employees. Records indicate that these individuals are proficient in several languages, including German, English, Spanish, and Italian. Further, the records show that personnel work in shifts to cater to various time zones, each having completed a robust training course pertaining to their respective geographic area's energy guidelines and client needs.

During 2025, it was documented that local staff successfully guided clients through more than 200 updates of regulatory nature in their corresponding markets without infractions being reported. The company provided in-depth information on the energy dynamics of each jurisdiction to which functions were transferred, as well as its respective environmental regulations.

Relating to procedural matters, the company executed a notification of business restructuring well ahead of the stipulated 16-week minimum period, as prescribed by German tax law. Said notification contained comprehensive details relating to the functions anticipated to be transferred, including schematic representations of the planned distribution among foreign entities. Further, the notification elaborated on provisions to maintain an uninterrupted energy supply during the transitional period.

Customer satisfaction metrics for the year under review, being specifically the fourth quarter of 2025, demonstrate a resolution rate of 90% for queries within the initial twenty-four hours. Detailed analysis of the transferred roles revealed that not all receiving foreign entities possessed experience or related expertise.

Case 2:
It has been established in the course of the review of the facts of the case that Gamma Innovations UG, operating in the energy supply and renewable energy sector, implemented a business restructuring. This restructuring saw a major function of Gamma Innovations UG being transferred from its central unit to a distribution center. Precisely, the function pertaining to the logistics calculus and the distribution of renewable energy projects underwent a shift in operation locus.

The records review indicates that the distribution center processed over 15,000 shipments related to renewable energy projects in the past fiscal year. It is worthy of note that the quantity of shipments handled by the distribution center witnessed a 50% increase, rising from 10,000 to 15,000 within a single fiscal year.

An examination of operational data over a three-year period reveals a progressively rising turnover at the distribution center, with an average annual increase of 20%. These operations involved the movement of more than 500 metric tons of inbound and outbound goods per operational day.

Despite the transfer of a significant function to the distribution center, it was identified that Gamma Innovations UG retained strategic control over general business operations. Furthermore, it was found that the distribution center, whilst part of Gamma Innovations UG, operated autonomously in executing its day-to-day activities.

A notable omission in provided documentation was that the specific valuation associated with the transferred function was absent. Moreover, a detailed logistical routing protocol, a key component in the analysis of the function transfer, was not made available in the submitted records.

It has been established through the study of the communication trail, or the lack thereof, that Gamma Innovations UG did not proactively inform the Finanzgericht Hamburg of the initiated business restructuring. It was during an unrelated audit, carried out by the Finanzgericht Hamburg, that the said restructuring was uncovered.

Which case is more likely to be accepted?

Pick one of the following choices:
1 - Case 1
2 - Case 2

You must pick one option. To determine which case is more likely to be accepted, analyze:
1. Applicable law: Is it clear or unclear?
2. Economic activity: Is it sufficient or insufficient?
3. Procedural requirements: Are they compliant or deficient?

A case with 2/3 elements satisfied (accept with conditions) is more favorable than 1/3 (fully reject).

Explain your reasoning step by step before you answer. Finally, the last thing you generate should be "ANSWER: (your answer here, including the choice number)"
""".strip()

reasoning = """
Let's analyze each case systematically by evaluating the three legal elements:

**Case 1 Analysis (TechStart Innovation UG):**

Applicable Law:
- The case involves transfer of unique functional roles (power grid connectivity, energy efficiency, renewable energy) across borders from Germany to multiple foreign entities
- The functions transferred are complex and require dedicated sector specialists
- Not all receiving foreign entities had experience or expertise in their new roles
- This complexity creates ambiguity under OECD Transfer Pricing Guidelines' provisions
- When unique roles with complex and specialist tasks are transferred in cross-border operations, accurate application of OECD TP Guidelines becomes contentious
→ Applicable law is UNCLEAR

Economic Activity:
- TechStart maintains a customer service hub with 30 full-time employees proficient in multiple languages (German, English, Spanish, Italian)
- Staff work in shifts covering different time zones and completed rigorous training for their geographic areas
- In 2025, local staff successfully guided clients through over 200 regulatory changes with no infractions reported
- Customer satisfaction metrics show 90% query resolution within 24 hours (Q4 2025)
- The company demonstrates local market proficiency and operational management capabilities
→ Economic activity is SUFFICIENT

Procedural Requirements:
- Business restructuring notification was delivered 16 weeks in advance (far exceeding the 6-week minimum)
- Notification contained comprehensive details about functions to be transferred with schematic representations
- Included information on energy dynamics of each jurisdiction and environmental regulations
- Elaborated on measures for maintaining uninterrupted energy supply during transition
→ Procedural requirements are COMPLIANT

Case 1 Result: 2/3 elements satisfied (sufficient economic activity + compliant procedures) → accept with conditions

**Case 2 Analysis (Gamma Innovations UG):**

Applicable Law:
- The case involves transfer of function (logistics calculus and renewable energy project distribution) to an autonomously operating distribution center
- The function was isolated to a separate entity while Gamma retained strategic control
- Classification between partial transfer vs complete relocation is unclear under § 1 Foreign Tax Act
- The degree of strategic control retained by parent company creates ambiguity in legal classification
→ Applicable law is UNCLEAR

Economic Activity:
- Distribution center processed over 15,000 renewable energy project shipments in the past fiscal year
- Shipment volume increased 50% (from 10,000 to 15,000) within one fiscal year
- Operational turnover increased 20% annually over three years
- Operations involved movement of 500+ metric tons of goods per operational day
- The high shipment volumes and growth trend demonstrate considerable economic activity
→ Economic activity is SUFFICIENT

Procedural Requirements:
- Gamma did not proactively inform Finanzgericht Hamburg of the business restructuring
- The restructuring was discovered only during an unrelated audit
- Specific valuation of the transferred function was not provided
- Detailed logistical routing protocol was not submitted
- Optimal regulatory compliance requires timely notification of significant structural changes
→ Procedural requirements are DEFICIENT

Case 2 Result: 1/3 elements satisfied (only sufficient economic activity) → fully reject

**Conclusion:**
Case 1 (TechStart Innovation UG) satisfies 2/3 elements with unclear law but sufficient economic activity and compliant procedures, resulting in "accept with conditions."

Case 2 (Gamma Innovations UG) satisfies only 1/3 elements with unclear law and sufficient economic activity but deficient procedures, resulting in "fully reject."

Therefore, Case 1 is significantly more likely to be accepted by the tax authority.

ANSWER: 1
""".strip()

german_tax_solved_ex = f'{story}\n\n{reasoning}'

