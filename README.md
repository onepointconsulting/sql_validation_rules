# SQL Validation Rules

This projects implements an agent which generates SQL validation rules for any database using an LLM.

## Install the project

```bash
conda remove -n sql_validation_rules --all
conda create -n sql_validation_rules python=3.12
conda activate sql_validation_rules
pip install poetry
poetry install
```

## Running unit tests

```bash
python -m unittest
```

## Running some integration tests

```bash
python .\sql_validation_rules\graph\graph_integration_test_cases.py
```