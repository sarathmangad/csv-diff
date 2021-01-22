import csv
import click
import json as std_json
from . import load_csv, compare, human_text


@click.command()
@click.version_option()
@click.argument(
    "previous",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, allow_dash=False),
)
@click.argument(
    "current",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, allow_dash=False),
)
@click.option(
    "--key", type=str, default=None, help="Column to use as a unique ID for each row"
)
@click.option(
    "--format",
    type=click.Choice(["csv", "tsv"]),
    default=None,
    help="Explicitly specify input format (csv, tsv) instead of auto-detecting",
)
@click.option(
    "--json", type=bool, default=False, help="Output changes as JSON", is_flag=True
)
@click.option(
    "--singular",
    type=str,
    default=None,
    help="Singular word to use, e.g. 'tree' for '1 tree'",
)
@click.option(
    "--plural",
    type=str,
    default=None,
    help="Plural word to use, e.g. 'trees' for '2 trees'",
)
@click.option(
    "--show-unchanged",
    is_flag=True,
    help="Show unchanged fields for rows with at least one change",
)
def cli(previous, current, key, format, json, singular, plural, show_unchanged):
    "Diff two CSV files"

    csv.register_dialect('excel-pipe', delimiter='|', quoting=csv.QUOTE_NONE)
    dialect = {
        "csv": "excel",
        "tsv": "excel-tab",
        "psv": "excel-pipe"
    }

    def load(filename):
        return load_csv(
            open(filename, newline=""), key=key, dialect=dialect.get(format)
        )

    diff = compare(load(previous), load(current), show_unchanged)
    if json:
        print(std_json.dumps(diff, indent=4))
    else:
        print(human_text(diff, key, singular, plural))
