from typing import List, Union
from pathlib import Path
import click
import json

from sql_validation_rules.tools.sql_tools import sql_query_columns, sql_list_tables
from sql_validation_rules.graph.graph_utils import (
    create_human_message,
    create_supervisor_message,
    invoke_column_rule,
    extract_sql_command,
    generate_supervisor_config,
)
from sql_validation_rules.config.config import logger
from sql_validation_rules.chain.sql_commands import SQLCommand
from sql_validation_rules.graph.supervisor_graph_factory import create_supervisor_app
from sql_validation_rules.agent.supervisor_factory import (
    VALIDATOR_MAIN_VALIDATOR,
    VALIDATOR_SQL_NUMERIC_VALIDATOR,
)


config = generate_supervisor_config()


@click.group()
@click.pass_context
def cli(ctx):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)


@cli.command()
@click.option(
    "-t",
    "--table",
    help="The table for which you want to generate the rules. You can use this option multiple times.",
)
@click.option("-f", "--file", help="The output file into which the output is recorded.")
@click.option("-h", "--hide_steps", help="Hide steps", is_flag=True, default=False)
@click.option(
    "--count",
    type=int,
    default=1,
    help="How many distinct rules to generate",
)
def generate_rules(table: str, file: str, hide_steps: bool, count: int):
    """Generates rules for all fields in a table"""

    output_file = Path(file)
    if output_file.exists():
        # rename the file
        pass
    with open(output_file, "w") as f:
        col_json = sql_query_columns(table)
        cols = json.loads(col_json)
        _, supervisor_app = create_supervisor_app()
        for i, col in enumerate(cols):
            sep = "\n\n" if i > 0 else ""
            col_name = col["name"]
            f.write(f"{sep}# {table} - {col_name}\n")
            inputs = create_human_message(create_supervisor_message(table, col_name))
            try:
                last_content = ""
                for content in supervisor_app.stream(inputs, config):
                    if not hide_steps:
                        f.write("\n -------------------- \n")
                        f.write(f"{content}")
                    if VALIDATOR_MAIN_VALIDATOR in content:
                        last_content += extract_sql_command(
                            content[VALIDATOR_MAIN_VALIDATOR]["messages"]
                        )
                    elif VALIDATOR_SQL_NUMERIC_VALIDATOR in content:
                        last_content += extract_sql_command(
                            content[VALIDATOR_SQL_NUMERIC_VALIDATOR]["messages"]
                        )
                    f.flush()

                f.write(f"\n\n{last_content}\n\n")
                f.flush()
            except Exception as e:
                msg = f"Failed to process {inputs}. Reason: {e}"
                logger.exception(msg)
                f.write(msg)


@cli.command()
def list_tables():
    """Lists all tables in a database."""
    all_tables = sql_list_tables("")
    for i, t in enumerate(all_tables.split(",")):
        print(f"{i + 1}. {t.strip()}")


@cli.command()
@click.option(
    "-t",
    "--table",
    help="The table for which you want to list the columns",
)
def list_columns(table: str):
    """Lists all columns in a table."""
    try:
        columns = sql_query_columns(table)
        col_list = json.loads(columns)
        print(f"\n{table}")
        for i in range(len(table)):
            print("=", end="")
        print("\n")
        for i, c in enumerate(col_list):
            print(f"{i + 1}. {c}")
        print("\n")
    except Exception as e:
        print(f"Error: {e}")
        print(
            f"Could not list list fields for table '{table}'. Does table '{table}' exist?"
        )


@cli.command()
@click.option(
    "-t",
    "--table",
    help="The table of the column for which you want to generate rules.",
)
@click.option(
    "-c",
    "--column",
    help="The column for which you want to generate rules.",
)
def generate_column_rule(table: str, column: str):
    "Generate a single rule for a column"
    res = invoke_column_rule(table, column, config)
    extraction_content = extract_sql_command(res["messages"])
    if extraction_content:
        print("Validation type:")
        print(extraction_content)
        print()
    else:
        print("No validation available.")


def extract_content(res: dict) -> Union[SQLCommand, None]:
    if len(res["extraction_content"]) > 0:
        extraction_content = res["extraction_content"][0]
        return extraction_content
    return None


if __name__ == "__main__":
    cli()
