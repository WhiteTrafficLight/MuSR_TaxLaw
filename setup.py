from setuptools import setup, find_packages

setup(
    name="musr-taxlaw",
    version="0.1.0",
    description="German Tax Law Case Generation using MuSR framework with CrewAI",
    author="Based on MuSR by Zayne Sprague et al.",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.70.0",
        "transformers>=4.51.0",
        "tqdm>=4.66.0",
        "numpy>=1.26.0",
        "redis>=5.0.0",
        "crewai>=0.201.0",
        "langchain>=0.3.25",
        "langchain-openai>=0.3.16",
        "langchain-core>=0.3.58",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
        ],
        "hf": [
            "torch>=2.0.0",
            "accelerate>=0.20.0",
        ]
    }
)
