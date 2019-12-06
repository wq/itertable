from . import load_file, load_url, flattened, JsonStringIter, CsvStringIter
from .exceptions import IterException
import click
import os
import importlib


@click.command()
@click.argument('source')
@click.argument('source_options', required=False)
@click.option('--format', '-f', default='csv', help='Output format')
def cat(source, source_options, format):
    """
    Display contents of a file or IterTable class.  SOURCE can be either a
    filename or a Python path.  SOURCE_OPTIONS is an optional string
    specifying init options in "name=value" format, separated by commas.

    The data will be printed to the terminal in CSV form, unless the format is
    set to JSON.

    Examples:

    \b
    python3 -m itertable example.json         # JSON to CSV
    python3 -m itertable -f json example.csv  # CSV to JSON
    python3 -m itertable example.xlsx "start_row=5"
    python3 -m itertable http://example.com/example.csv
    python3 -m itertable itertable.CsvNetIter "url=http://example.com/example.csv"
    """  # noqa

    # Parse option string
    options = {}
    if source_options:
        for opt in source_options.split(','):
            key, val = opt.split('=')
            if val.isdigit():
                val = int(val)
            options[key] = val

    if os.path.exists(source):
        try:
            input = load_file(source, options=options)
        except IterException as e:
            raise click.ClickException(str(e))
    elif 'http' in source and '://' in source:
        try:
            input = load_url(source, options=options)
        except IterException as e:
            raise click.ClickException(str(e))
    else:
        parts = source.split('.')
        class_name = parts[-1]
        module_name = ".".join(parts[:-1])
        try:
            module = importlib.import_module(module_name)
            Iter = getattr(module, class_name)
            input = flattened(Iter, **options)
        except (ImportError, ValueError, AttributeError, IterException) as e:
            raise click.ClickException(str(e))

    if format == "json":
        OutputIter = JsonStringIter
        init = "[]"
    else:
        OutputIter = CsvStringIter
        init = ""
    output = OutputIter(data=input.data, string=init)
    output.data = input.data
    output.save()
    result = output.string
    if output.binary:
        result = result.decode('utf-8')
    print(result)
