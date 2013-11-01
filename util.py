from wq.io.base import BaseIO
from wq.io.loaders import FileLoader, BinaryFileLoader, NetLoader, StringLoader
from wq.io.parsers import CsvParser, JsonParser, XmlParser, ExcelParser
from wq.io.mappers import TupleMapper
import mimetypes

PARSERS = {
    'application/vnd.ms-excel': ExcelParser,
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
    ExcelParser,
    'text/csv': CsvParser,
    'application/json': JsonParser,
    'application/xml': XmlParser,
}
BINARY_FORMATS = (
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
)


def make_io(loader, parser, mapper=TupleMapper, name=None):
    if name is None:
        lname = parser.__name__.replace('Parser', '')
        pname = loader.__name__.replace('Loader', '')
        if mapper == TupleMapper:
            mname = ""
        else:
            mname = mapper.__name__.replace('Mapper', '')
        name = lname + pname + mname + "IO"
    return type(name, (loader, parser, mapper, BaseIO), {})


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
        raise Exception("Could not determine parser for %s" % mimetype)
    parser = PARSERS[mimetype]
    loader = BinaryFileLoader if mimetype in BINARY_FORMATS else FileLoader
    IO = make_io(loader, parser, mapper)
    return IO(filename=filename, **options)


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
    return IO(string=string, **options)
