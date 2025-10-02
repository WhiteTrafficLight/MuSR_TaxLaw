# MuSR-TaxLaw: German Tax Law Case Generation

### A modified version of MuSR for generating German tax law cases that require multi-step legal reasoning

**Based on the original MuSR framework by Zayne Sprague, Xi Ye, Kaj Bostrom, Swarat Chaudhuri, and Greg Durrett.**

This repository is a fork and adaptation of the original [MuSR project](https://zayne-sprague.github.io/MuSR/) ([paper](https://arxiv.org/abs/2310.16049), ICLR 2024) specifically modified for generating complex German tax law cases. The original MuSR framework has been adapted to create legal reasoning scenarios in the domain of German tax law.

**Original Authors:** zayne@utexas.edu {xi, kaj, swarat, gdurrett}@cs.utexas.edu

**Modifications:** This fork modifies the domain-specific components, sampling logic, and prompting strategies to generate German tax law cases while preserving the core MuSR reasoning framework.

<image src="./imgs/logo.png"></image>

## German Tax Law Case Evaluation

The datasets are in `datasets/german_tax_law_case.json` and `datasets/german_tax_law_case2.json`

### Install

1. `virtualenv venv` we have tested with python 3.8
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`

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

### New models

Right now we support all the OpenAI endpoints and models published on Huggingface.  

Custom models made in PyTorch or Tensorflow will need to have an implementation that follows from the `Model` class in `src/model/model.py` similar to `src/model/hf.py` (for Huggingface).  

### New prompts and MuSR domain datasets

These are easily added to the `eval/eval.py` file.


## Overview of MuSR-TaxLaw

<image src="./imgs/system_diagram.png"></image>

This repository is a modified version of the original MuSR framework, adapted for generating German tax law cases that require multi-step legal reasoning. The original MuSR methodology has been preserved while the domain-specific components have been replaced with German tax law elements.

German tax law case datasets can be found in `{project_root}/datasets`. The domain-specific seed data for generating tax law scenarios is located in `{project_root}/domain_seed/`.

Major components for making the MuSR dataset can be found in `{project_root}/src`.  

Important classes and structures will have some example uses in their files (Madlib and LogicTree for example)

The scripts used to create a dataset can be found in `{project_root}/musr_dataset_scripts`

Evaluation scripts are in `{project_root}/eval`


## Generating German Tax Law Case Datasets

The German tax law case creation script is in `{project_root}/musr_dataset_scripts/create_german_tax_law_case.py`. This script contains detailed instructions on how to create German tax law case datasets with various parameters for customization.

To run the script:

```shell
cd musr_dataset_scripts
OPENAI_API_KEY=key python musr_dataset_scripts/create_german_tax_law_case.py
```
NOTE: This has been tested with GPT-4. Quality may significantly degrade if you use a different model due to the prompts being heavily tailored to GPT-4 and the requirement for strict formatting in legal reasoning outputs.

This will produce a German tax law case dataset file in `{project_root}/datasets` after it completes.

## Creating your own dataset

You can implement your own DatasetBuilder following the examples for the other domains.

For example, the important files used in creating German tax law cases are:

`{project_root}/src/dataset_builder.py`: The main file used for creating all datasets (shared functionality including the recursive reasoning tree expansion algorithm).

`{project_root}/src/dataset_types/german_tax_dataset.py`: Specific domain logic (and some prompts) for creating the German tax law cases.

`{project_root}/musr_dataset_scripts/create_german_tax_law_case.py`: The main file that glues everything together (and includes some more prompts).

`{project_root}/domain_seed/`: Contains domain-specific seed data for German tax law scenarios, including business sectors, transaction types, tax authorities, and various compliance scenarios. 
