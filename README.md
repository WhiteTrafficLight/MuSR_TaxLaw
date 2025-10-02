# MuSR-TaxLaw: German Tax Law Case Generation

### A modified version of MuSR for generating German tax law cases that require multi-step legal reasoning

**Based on the original MuSR framework by Zayne Sprague, Xi Ye, Kaj Bostrom, Swarat Chaudhuri, and Greg Durrett.**

This repository is a fork and adaptation of the original [MuSR project](https://zayne-sprague.github.io/MuSR/) ([paper](https://arxiv.org/abs/2310.16049), ICLR 2024) specifically modified for generating complex German tax law cases. The original MuSR framework has been adapted to create legal reasoning scenarios in the domain of German tax law.

**Original Authors:** zayne@utexas.edu {xi, kaj, swarat, gdurrett}@cs.utexas.edu

**Modifications:** This fork modifies the domain-specific components, sampling logic, and prompting strategies to generate German tax law cases while preserving the core MuSR reasoning framework.

## German Tax Law Case Evaluation

The datasets are in `datasets/german_tax_law_case.json` and `datasets/german_tax_law_case2.json`

### Install

**Note**: The project has been tested with the `taxlaw` conda environment using Python 3.10.

**Option 1: Using Conda with Editable Install (Recommended)**
1. `conda create -n taxlaw python=3.10`
2. `conda activate taxlaw`
3. `pip install -e .`

**Option 2: Using Virtual Environment with Editable Install**
1. `virtualenv venv` (tested with python 3.10)
2. `source venv/bin/activate`
3. `pip install -e .`

**Option 3: Manual Requirements Install**
1. Create and activate your environment (conda or virtualenv)
2. `pip install -r requirements.txt`


### Evaluate


To run the evaluation script on the German tax law case datasets:
```shell
cd eval
OPENAI_API_KEY=key python eval.py
```

You can edit the functionality of the evaluation in eval.py as well (including different prompting strategies, models, and more).

### [Optional] Install Redis for caching  

We cache all LLM calls (openai and huggingface) with keys based on the prompt and model parameters to speed up evaluations.

To do this, we used [Redis](https://redis.io/docs/clients/python/)

Easiest way to install it is (for linux)
1. `apt-get install redis`
2. `redis-server`

Alternatively you can run our code without redis or disable the cache entirely by commenting out the lines `cache.enable()`.

### CrewAI Integration for Modular Prompt Management

Unlike the murder mystery domain which uses a single prompt for tree node expansion, German tax law case domain requires component and depth-specific prompts. Therefore, we integrated CrewAI for dynamic prompt management and made structural changes to the `src` directory.

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




## Overview of MuSR-TaxLaw

<image src="./imgs/system_diagram.png"></image>

This repository is a modified version of the original MuSR framework, adapted for generating German tax law cases that require multi-step legal reasoning. The original MuSR methodology has been preserved while the domain-specific components have been replaced with German tax law elements.

German tax law case datasets can be found in `{project_root}/datasets`. The domain-specific seed data for generating tax law scenarios is located in `{project_root}/domain_seed/`.

Major components for making the German tax law datasets can be found in `{project_root}/src`, with the following structure:

```
src/
├── crews/                    # CrewAI integration for multi-agent reasoning
│   ├── agents.py            # Specialized agents (legal, economic, procedural)
│   ├── tasks.py             # Task definitions for reasoning components
│   ├── config/prompts/      # Modular prompt templates
│   │   ├── law.py          # Legal reasoning prompts
│   │   ├── econ.py         # Economic analysis prompts
│   │   ├── proc.py         # Procedural compliance prompts
│   │   └── story.py        # Narrative generation prompts
│   ├── tree_builder.py     # CrewAI-integrated tree expansion
│   └── runner.py           # Multi-agent orchestration
├── dataset_types/          # Domain-specific dataset logic
│   └── german_tax_dataset.py
├── logic_tree/             # Core reasoning tree structure
├── model/                  # LLM interface abstractions
├── utils/                  # Utility functions and caching
└── validators/             # Output validation logic
```

Important classes and structures will have some example uses in their files (Madlib and LogicTree for example)

The scripts used to create a dataset can be found in `{project_root}/musr_dataset_scripts`

Evaluation scripts are in `{project_root}/eval`


## Generating German Tax Law Case Datasets

The German tax law case creation script is in `{project_root}/musr_dataset_scripts/create_german_tax_law_case.py`. This script contains detailed instructions on how to create German tax law case datasets with various parameters for customization.

To run the script:

```shell
OPENAI_API_KEY=key python musr_dataset_scripts/create_german_tax_law_case.py
```

**Model Configuration:**
Agent models can be configured in `src/crews/runner.py`:
- **Main generation model** (lines 43-53): Used for tree expansion and story generation
- **Validation models** (lines 59-78): Used for LLM-based validation when `--use-model-validator` flag is enabled
- **CrewAI agent models**: Configured in `src/crews/agents.py` functions `create_tree_agent()` and `create_story_agent()`

To use different models, modify the `engine` parameter in the respective `OpenAIModel` configurations or the `model` parameter in agent creation functions.

**Advanced Usage:**
```shell
# Use LLM-based validation (more accurate but expensive)
OPENAI_API_KEY=key python musr_dataset_scripts/create_german_tax_law_case.py --use-model-validator
```

NOTE: This has been tested with GPT-4. Quality may significantly degrade if you use a different model due to the prompts being heavily tailored to GPT-4 and the requirement for strict formatting in legal reasoning outputs.

This will produce a German tax law case dataset file in `{project_root}/datasets` after it completes.

### Viewing Generated Cases

After running the dataset generation script, you can view the generated German tax law cases in an interactive HTML format:

- **HTML Visualization**: Open `german_tax_law_case.html` in your browser to see a side-by-side comparison of generated tax law cases
- **Features**: 
  - Interactive reasoning tree visualization with collapsible nodes
  - Detailed case stories and metadata
  - Color-coded fact types (explicit vs. commonsense knowledge)
  - Question-answer format for evaluation

The HTML file provides a comprehensive view of:
- Business sector and transaction type context
- Taxpayer and tax authority information
- Decision outcomes (accept with conditions, fully reject, etc.)
- Complete reasoning trees with logical operators
- Generated court decision narratives

### Example Generated Case

You can see an example of the generated German tax law cases by opening [assets/german_tax_law_case_ex.html](assets/german_tax_law_case_ex.html) in your browser.



