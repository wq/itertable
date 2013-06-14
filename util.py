from wq.io.base    import BaseIO
from wq.io.loaders import FileLoader, BinaryFileLoader, NetLoader
from wq.io.parsers import CsvParser, JsonParser, XmlParser, ExcelParser
from wq.io.mappers import TupleMapper
import mimetypes

PARSERS = {
    'application/vnd.ms-excel': ExcelParser,
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ExcelParser,
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
        mname = "" if mapper == TupleMapper else mapper.__name__.replace('Mapper', '')
        name = lname + pname + mname + "IO"
    return type(name, (loader, parser, mapper, BaseIO), {})

def guess_type(filename):
    mimetype, encoding = mimetypes.guess_type(filename)
    if mimetype is None:
        try:
            import magic
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
