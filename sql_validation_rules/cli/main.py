from typing import List
from pathlib import Path
import click
import json

from sql_validation_rules.tools.sql_tools import sql_query_columns, sql_list_tables
from sql_validation_rules.graph.graph_utils import stream_outputs
from sql_validation_rules.config.config import logger
from sql_validation_rules.chain.sql_commands import SQLCommand


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
def generate_rules(table: str, file: str, hide_steps: bool):
    """Generates rules for all fields in a table"""
    output_file = Path(file)
    if output_file.exists():
        # rename the file
        pass
    with open(output_file, "w") as f:
        col_json = sql_query_columns(table)
        cols = json.loads(col_json)
        for i, col in enumerate(cols):
            inputs = {"table": table, "field": col["name"], "chat_history": []}
            sep = "\n\n" if i > 0 else ""
            f.write(f"{sep}# {inputs['table']} - {inputs['field']}\n")
            try:
                last_content = ""
                for content in stream_outputs(inputs):
                    if not hide_steps:
                        f.write("\n -------------------- \n")
                        f.write(f"{content}")
                    if "extraction_content" in content:
                        sql_commands: List[SQLCommand] = content["extraction_content"]
                        last_content = "\n".join([repr(s) for s in sql_commands])
                    f.flush()

                f.write(f"\n\n{last_content}\n\n")
                f.flush()
            except Exception as e:
                msg = f"Failed to process {inputs}. Reason: {e}"
                logger.exception(msg)
                f.write(msg)



@cli.command()
def list_tables():
    """Lists all table"""
    all_tables = sql_list_tables("")
    for i, t in enumerate(all_tables.split(",")):
        print(f"{i + 1}. {t.strip()}")

if __name__ == "__main__":
    cli()
