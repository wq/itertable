from wq.io.base import BaseIO
from wq.io.loaders import FileLoader, NetLoader, StringLoader
from wq.io.parsers import CsvParser, JsonParser, XmlParser, ExcelParser
from wq.io.mappers import TupleMapper
from wq.io.exceptions import ParseFailed
import mimetypes

PARSERS = {
    'application/vnd.ms-excel': ExcelParser,
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
    ExcelParser,
    'text/csv': CsvParser,
    'application/json': JsonParser,
    'application/xml': XmlParser,
}

# Save generated classes to avoid recreating them
_io_classes = {}


def make_io(loader, parser, mapper=TupleMapper, name=None, module="wq.io"):
    """
    Mix the specified loader, parser, and mapper classes into a usable IO
    """
    key = (loader, parser, mapper)
    if key in _io_classes:
        return _io_classes[key]

    if name is None:
        lname = parser.__name__.replace('Parser', '')
        pname = loader.__name__.replace('Loader', '')
        if mapper == TupleMapper:
            mname = ""
        else:
            mname = mapper.__name__.replace('Mapper', '')
        name = lname + pname + mname + "IO"
    cls = type(name, (loader, parser, mapper, BaseIO), {})
    cls.__module__ = module
    _io_classes[key] = cls
    return cls


def guess_type(filename, buffer=None):
    mimetype, encoding = mimetypes.guess_type(filename)
    if mimetype is None:
        try:
            import magic
            if buffer:
                mimetype = magic.from_buffer(buffer, mime=True)
            else:
                mimetype = magic.from_file(filename, mime=True)
        except ImportError:
            pass
    return mimetype


def load_file(filename, mapper=TupleMapper, options={}):
    mimetype = guess_type(filename)
    if mimetype not in PARSERS:
        raise ParseFailed("Could not determine parser for %s" % mimetype)
    parser = PARSERS[mimetype]
    loader = FileLoader
    IO = make_io(loader, parser, mapper)
    return IO(filename=filename, **options)


def load_url(url, mapper=TupleMapper, options={}):
    mimetype = guess_type(url)
    if mimetype not in PARSERS:
        raise ParseFailed("Could not determine parser for %s" % mimetype)
    parser = PARSERS[mimetype]
    loader = NetLoader
    IO = make_io(loader, parser, mapper)
    return IO(url=url, **options)


def load_string(string, mapper=TupleMapper, options={}):
    if string.startswith('<'):
        parser = XmlParser
    elif string.startswith('[') or (
            string.startswith('{') and 'namespace' in options):
        parser = JsonParser
    elif ',' in string:
        parser = CsvParser
    else:
        raise Exception("Could not determine parser for string!")

    loader = StringLoader
    IO = make_io(loader, parser, mapper)
    if IO.binary:
        string = string.encode('utf-8')
    return IO(string=string, **options)


class FlatIO(TupleMapper, BaseIO):
    """
    Denormalizes a nested IO structure (e.g. an array of individual time
    series) into a single iterable.  Each row in the top level IO should have
    an attribute (typically 'data') pointing to an inner IO.  Both the top
    level IO class and the inner class should extend TupleMapper.
    """

    io_class = None
    inner_attr = 'data'

    def __init__(self, *args, **kwargs):
        self.io_class = kwargs.pop('io_class', self.io_class)
        self.inner_attr = kwargs.pop('inner_attr', self.inner_attr)
        if self.io_class is None:
            raise Exception("An IO class must be specified")

        # Pass remaining arguments
        self.nested_io = self.io_class(*args, **kwargs)
        self.data = list(self.unpack_io())

    def unpack_io(self):
        # Loop through outer IO (e.g. metadata series)
        for outer in self.nested_io:
            meta = outer._asdict()
            inner_io = meta.pop(self.inner_attr)

            # Loop through inner IO (e.g. time series) on each record
            for inner in inner_io:
                record = meta.copy()
                record.update(inner._asdict())
                yield record


def flattened(io_class, *args, **kwargs):
    if io_class.nested:
        return FlatIO(io_class=io_class, *args, **kwargs)
    else:
        return io_class(*args, **kwargs)
