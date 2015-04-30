from wq.core import wq
from . import load_file, flattened, JsonStringIO, CsvStringIO
import click
import os
import importlib


@wq.command()
@click.argument('source')
@click.argument('source_options', required=False)
@click.option('--format', '-f', default='csv', help='Output format')
def cat(source, source_options, format):
    """
    Display contents of a file or wq.io class
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
        input = load_file(source, options=options)
    else:
        parts = source.split('.')
        class_name = parts[-1]
        module_name = ".".join(parts[:-1])
        module = importlib.import_module(module_name)
        IO = getattr(module, class_name)
        input = flattened(IO, **options)

    if format == "json":
        OutputIO = JsonStringIO
        init = "[]"
    else:
        OutputIO = CsvStringIO
        init = ""
    output = OutputIO(data=input.data, string=init)
    output.data = input.data
    output.save()
    print(output.string)
