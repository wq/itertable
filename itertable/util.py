from .base import BaseIter
from .loaders import FileLoader, NetLoader, StringLoader
from .parsers import CsvParser, JsonParser, XmlParser, ExcelParser
from .mappers import TupleMapper
from .exceptions import ParseFailed
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
_iter_classes = {}


def make_iter(loader, parser, mapper=TupleMapper,
              name=None, module="itertable"):
    """
    Mix the specified loader, parser, and mapper classes into a usable Iter
    """
    key = (loader, parser, mapper)
    if key in _iter_classes:
        return _iter_classes[key]

    if name is None:
        lname = parser.__name__.replace('Parser', '')
        pname = loader.__name__.replace('Loader', '')
        if mapper == TupleMapper:
            mname = ""
        else:
            mname = mapper.__name__.replace('Mapper', '')
        name = lname + pname + mname + "Iter"
    cls = type(name, (loader, parser, mapper, BaseIter), {})
    cls.__module__ = module
    _iter_classes[key] = cls
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
    Iter = make_iter(loader, parser, mapper)
    return Iter(filename=filename, **options)


def load_url(url, mapper=TupleMapper, options={}):
    mimetype = guess_type(url)
    if mimetype not in PARSERS:
        raise ParseFailed("Could not determine parser for %s" % mimetype)
    parser = PARSERS[mimetype]
    loader = NetLoader
    Iter = make_iter(loader, parser, mapper)
    return Iter(url=url, **options)


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
    Iter = make_iter(loader, parser, mapper)
    if Iter.binary:
        string = string.encode('utf-8')
    return Iter(string=string, **options)


class FlatIter(TupleMapper, BaseIter):
    """
    Denormalizes a nested Iter structure (e.g. an array of individual time
    series) into a single iterable.  Each row in the top level Iter should have
    an attribute (typically 'data') pointing to an inner Iter.  Both the top
    level Iter class and the inner class should extend TupleMapper.
    """

    iter_class = None
    inner_attr = 'data'

    def __init__(self, *args, **kwargs):
        self.iter_class = kwargs.pop('iter_class', self.iter_class)
        self.inner_attr = kwargs.pop('inner_attr', self.inner_attr)
        if self.iter_class is None:
            raise Exception("An Iter class must be specified")

        # Pass remaining arguments
        self.nested_iter = self.iter_class(*args, **kwargs)
        self.data = list(self.unpack_iter())

    def unpack_iter(self):
        # Loop through outer Iter (e.g. metadata series)
        for outer in self.nested_iter:
            meta = outer._asdict()
            inner_iter = meta.pop(self.inner_attr)

            # Loop through inner Iter (e.g. time series) on each record
            for inner in inner_iter:
                record = meta.copy()
                record.update(inner._asdict())
                yield record


def flattened(iter_class, *args, **kwargs):
    if iter_class.nested:
        return FlatIter(iter_class=iter_class, *args, **kwargs)
    else:
        return iter_class(*args, **kwargs)
