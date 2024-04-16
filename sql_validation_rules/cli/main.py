from typing import List
from pathlib import Path
import click
import json

from sql_validation_rules.tools.sql_tools import sql_query_columns
from sql_validation_rules.graph.graph_utils import stream_outputs


@click.command()
@click.option(
    "-t",
    "--table",
    help="The table for which you want to generate the rules. You can use this option multiple times.",
    multiple=True,
)
@click.option("-f", "--file", help="The output file into which the output is recorded.")
def generate_rules(table: List[str], file: str):
    """Generates rules for all fields in a table"""
    output_file = Path(file)
    if output_file.exists():
        # rename the file
        pass
    with open(output_file, "w") as f:
        for t in table:
            col_json = sql_query_columns(t)
            cols = json.loads(col_json)
            for i, col in enumerate(cols):
                inputs = {"table": t, "field": col['name'], "chat_history": []}
                f.write(f"{"\n\n" if i > 0 else ""}# {inputs['table']} - {inputs['field']}\n")
                try:
                    last_content = ''
                    for content in stream_outputs(inputs):
                        f.write("\n -------------------- \n")
                        f.write(f"{content}")
                        if 'extraction_content' in content:
                            last_content = "\n".join(content['extraction_content'])
                    f.write(f"\n\n{last_content}\n\n")
                except Exception as e:
                    f.write(f"Failed to process {inputs}. Reason: {e}")
                


if __name__ == "__main__":
    generate_rules()
