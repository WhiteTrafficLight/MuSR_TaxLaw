# MuSR-TaxLaw: German Tax Law Case Generation

### A modified version of MuSR for generating German tax law cases that require multi-step legal reasoning

**Based on the original MuSR framework by Zayne Sprague, Xi Ye, Kaj Bostrom, Swarat Chaudhuri, and Greg Durrett.**

This repository is a fork and adaptation of the original [MuSR project](https://zayne-sprague.github.io/MuSR/) ([paper](https://arxiv.org/abs/2310.16049), ICLR 2024) specifically modified for generating complex German tax law cases. The original MuSR framework has been adapted to create legal reasoning scenarios in the domain of German tax law.

**Original Authors:** zayne@utexas.edu {xi, kaj, swarat, gdurrett}@cs.utexas.edu

**Modifications:** This fork modifies the domain-specific components, sampling logic, and prompting strategies to generate German tax law cases while preserving the core MuSR reasoning framework.

## Installation & Setup

**Note**: The project has been tested with Python 3.10.

**Option 1: Using Conda with Editable Install (Recommended)**
1. `conda create -n myenv python=3.10`
2. `conda activate myenv`
3. `pip install -e .`
4. Copy `.env.example` to `.env` and add your OpenAI API key

**Option 2: Using Virtual Environment with Editable Install**
1. `virtualenv venv` (tested with python 3.10)
2. `source venv/bin/activate`
3. `pip install -e .`
4. Copy `.env.example` to `.env` and add your OpenAI API key

**Option 3: Manual Requirements Install**
1. Create and activate your environment (conda or virtualenv)
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your OpenAI API key


## Evaluation

To run the evaluation script on the German tax law case datasets:
```shell
python eval/eval.py
```

You can edit the functionality of the evaluation in eval.py as well (including different prompting strategies, models, and more).

## Generating German Tax Law Case Datasets

The German tax law case creation script is in `{project_root}/musr_dataset_scripts/create_german_tax_law_case.py`.

To run the script:

```shell
python musr_dataset_scripts/create_german_tax_law_case.py
```
The generated dataset will be saved in `datasets/german_tax_law_case.json`

`german_tax_law_case.html` will be generated in the root directory which visualizes the generated law case and the reasoning tree. 

## Key Implementation

### Domain Seed Replacement

<p align="center">
  <img src="./assets/tree_comparison.png" alt="Tree Comparison between Murder Mystery & Tax Law Case" width="1000"/>
</p>

Replaced murder mystery MMO (Motivation, Means, Opportunity) components and related domain seed with LEP (Applicable Law, Economic Activity, Procedural Requirements).
To make the created law cases suitable for LLM reasoning, we merged two different law cases and set a question asking which one is more likely to be accepted. 

[Check created example law cases & example question](https://whitetrafficlight.github.io/MuSR_TaxLaw/)

### CrewAI Integration for Modular Prompt Management

Unlike the murder mystery domain which uses a single prompt for tree node expansion, the German tax law case domain requires component and depth-specific prompts. Therefore, we integrated CrewAI for dynamic prompt management and made structural changes to the `src` directory.

The new `src/crews/` directory contains:
- **agents.py**: Specialized agents for different aspects of tax law reasoning (legal, economic, procedural)
- **tasks.py**: Task definitions for different reasoning components
- **config/prompts/**: Modular prompt templates organized by domain:
  - `law.py`: Legal reasoning prompts
  - `econ.py`: Economic analysis prompts  
  - `proc.py`: Procedural compliance prompts
  - `story.py`: Narrative generation prompts
- **tree_builder.py**: CrewAI-integrated tree expansion logic
- **runner.py**: Orchestrates the multi-agent reasoning process

## Dataset Structure

The generated datasets follow this structure:
```json
{
  "id": "case_001",
  "business_sector": "energy supply",
  "transaction_type": "function_transfer", 
  "question": "Which case should be accepted?",
  "choices": ["Case A", "Case B"],
  "answer": "Case A",
  "cases": [
    {
      "taxpayer": "Company Name",
      "tax_authority": "Authority Name", 
      "decision": "accept with conditions",
      "reasoning_tree": "...",
      "story": "Court decision narrative..."
    }
  ]
}
```

## Configuration

**Model Settings**: Modify models in `src/crews/runner.py`
- Main generation: GPT-4 (lines 43-53)
- Validation: GPT-4 + GPT-3.5-turbo (lines 59-78)

**Advanced Options**:
```shell
# Enable LLM-based validation (more accurate but expensive)
PYTHONPATH=. python musr_dataset_scripts/create_german_tax_law_case.py --use-model-validator
```





