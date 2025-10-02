"""
CrewAI entry script: generate one German tax law case using Crew-guided tasks.

Run with:
  # Basic mode (Structure + Forbidden validators only)
  PYTHONPATH=. python musr_dataset_scripts/create_german_tax_law_case.py
  
  # Advanced mode (with LLM-based validation - more accurate but expensive)
  PYTHONPATH=. python musr_dataset_scripts/create_german_tax_law_case.py --use-model-validator

Make sure to set OPENAI_API_KEY in your .env file.
"""

import argparse
from dotenv import load_dotenv
from src.crews.runner import run_single_german_tax_case

# Load environment variables from .env file
load_dotenv()


def main():
    parser = argparse.ArgumentParser(description='Generate German tax case with CrewAI')
    parser.add_argument(
        '--use-model-validator',
        action='store_true',
        help='Use LLM-based validation for element purity (more accurate but expensive)'
    )
    args = parser.parse_args()
    
    print(f"Starting German tax case generation...")
    if args.use_model_validator:
        print("Model validator enabled: This will be more accurate but significantly more expensive!")
    else:
        print("Using basic validators (Structure + Forbidden text)")
    
    run_single_german_tax_case(use_model_validator=args.use_model_validator)


if __name__ == "__main__":
    main()


