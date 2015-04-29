from wq.core import wq
from . import load_file, CsvStringIO
import click


@wq.command()
@click.argument('source')
def cat(source):
    """
    Display contents of a file in CSV format
    """
    input = load_file(source)
    output = CsvStringIO(data=input.data)
    output.data = input.data
    output.save()
    print(output.string)
