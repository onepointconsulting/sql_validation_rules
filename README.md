# SQL Validation Rules

This projects implements an agent which generates SQL validation rules for any database using an LLM.

## Install the project

Please make sure that Conda is properly installed on your shell. Typically you can install

```bash
conda remove -n sql_validation_rules --all
conda create -n sql_validation_rules python=3.12
conda activate sql_validation_rules
pip install poetry
poetry install
```

## Configuration

Please check the [.env_local](.env_local) file to see the needed configuration parameters. 
You should copy this file to `.env` and then fill the necessary parameters. Please note that this tool requires a valid ChatGPT API key.

## Running unit tests

```bash
python -m unittest
```

## Running some integration tests

```bash
python ./sql_validation_rules/graph/graph_integration_test_cases.py
```

## Running the command line tool

View the supported commands:

```bash
python .\sql_validation_rules\cli\main.py --help
```

List all columns of table 'call_center':

```bash
python .\sql_validation_rules\cli\main.py list-columns --table call_center
```

Generate validation rules for table inventory:

```bash
python ./sql_validation_rules/cli/main.py generate-rules --table inventory -f inventory.txt
python ./sql_validation_rules/cli/main.py generate-rules --table inventory -f inventory.txt --hide_steps
python ./sql_validation_rules/cli/main.py generate-rules --table inventory -f inventory.txt --hide_steps --count 2
```

Generate validation rules for table call_center:

```bash
python .\sql_validation_rules\cli\main.py generate-rules -t call_center -f call_center.txt
```

Generate validation rule for a specific column in a table excluding some rule types:

```bash
python ./sql_validation_rules/cli/main.py generate-column-rule --table call_center -c cc_call_center_sk -e "Data Type Validation, Validation SQL"
```

Generate multiple rules for one single table column:

```bash
python ./sql_validation_rules/cli/main.py generate-multiple-column-rules --table call_center -c cc_call_center_sk --count 4 -f call_center_cc_call_center_sk.md
```

```bash
python ./sql_validation_rules/cli/main.py generate-multiple-column-rules --table call_center -c cc_city --count 3 -f call_center_cc_city.txt
```

## Running the Streamlit app

With the in-built Streamlit UI you can select a table and a column and then generate rules for it using the supervisor agent.
You can start the user interface using the following command:

```bash
streamlit run ./sql_validation_rules/ui/streamlit_main.py
```

On Windows you can start the user interface by executing this script:

```ps1
.\start_ui.ps1
```