from wq.core import wq
from . import load_file, load_url, flattened, JsonStringIO, CsvStringIO
from .exceptions import IoException
import click
import os
import importlib


@wq.command()
@click.argument('source')
@click.argument('source_options', required=False)
@click.option('--format', '-f', default='csv', help='Output format')
def cat(source, source_options, format):
    """
    Display contents of a file or wq.io class.  SOURCE can be either a filename
    or a Python path.  SOURCE_OPTIONS is an optional string specifying init
    options in "name=value" format, separated by commas.

    The data will be printed to the terminal in CSV form, unless the format is
    set to JSON.

    Examples:

    \b
    wq cat example.json
    wq cat example.xlsx "start_row=5"
    wq cat http://example.com/example.csv
    wq cat wq.io.CsvNetIO "url=http://example.com/example.csv"
    """

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
        except IoException as e:
            raise click.ClickException(str(e))
    elif 'http' in source and '://' in source:
        try:
            input = load_url(source, options=options)
        except IoException as e:
            raise click.ClickException(str(e))
    else:
        parts = source.split('.')
        class_name = parts[-1]
        module_name = ".".join(parts[:-1])
        try:
            module = importlib.import_module(module_name)
            IO = getattr(module, class_name)
            input = flattened(IO, **options)
        except (ImportError, ValueError, AttributeError, IoException) as e:
            raise click.ClickException(str(e))

    if format == "json":
        OutputIO = JsonStringIO
        init = "[]"
    else:
        OutputIO = CsvStringIO
        init = ""
    output = OutputIO(data=input.data, string=init)
    output.data = input.data
    output.save()
    result = output.string
    if output.binary:
        result = result.decode('utf-8')
    print(result)
