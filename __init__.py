from .base import BaseIO

from .loaders import (
    BaseLoader,
    FileLoader,
    Zipper,
    ZipFileLoader,
    StringLoader,
    NetLoader,
    ZipNetLoader,
)

from .parsers import (
    CsvParser,
    JsonParser,
    XmlParser,
    ExcelParser,
)

from .mappers import (
    BaseMapper,
    DictMapper,
    TupleMapper,
    TimeSeriesMapper,
    make_date_mapper,
)

from .util import (
    make_io,
    load_file,
    load_url,
    load_string,
    guess_type,
    flattened
)

from wq.io.version import VERSION


__all__ = (
    'BaseIO',

    'BaseLoader',
    'FileLoader',
    'Zipper',
    'ZipFileLoader',
    'StringLoader',
    'NetLoader',
    'ZipNetLoader',

    'CsvParser',
    'JsonParser',
    'XmlParser',
    'ExcelParser',

    'BaseMapper',
    'DictMapper',
    'TupleMapper',
    'TimeSeriesMapper',
    'make_date_mapper',

    'make_io',
    'load_file',
    'load_url',
    'load_string',
    'guess_type',
    'flattened',

    'VERSION',

    'CsvFileIO',
    'CsvNetIO',
    'CsvStringIO',

    'JsonFileIO',
    'JsonNetIO',
    'JsonStringIO',

    'XmlFileIO',
    'XmlNetIO',
    'XmlStringIO',

    'ExcelFileIO',
)

# Some useful pre-mixed classes
CsvFileIO = make_io(FileLoader, CsvParser)
CsvNetIO = make_io(NetLoader, CsvParser)
CsvStringIO = make_io(StringLoader, CsvParser)

JsonFileIO = make_io(FileLoader, JsonParser)
JsonNetIO = make_io(NetLoader, JsonParser)
JsonStringIO = make_io(StringLoader, JsonParser)

XmlFileIO = make_io(FileLoader, XmlParser)
XmlNetIO = make_io(NetLoader, XmlParser)
XmlStringIO = make_io(StringLoader, XmlParser)

ExcelFileIO = make_io(FileLoader, ExcelParser)
ExcelNetIO = make_io(NetLoader, ExcelParser)

try:
    from wq.io.gis import GisIO, ShapeIO, WktIO
    __all__ += (
        'GisIO',
        'ShapeIO',
        'WktIO',
    )
except ImportError:
    pass
