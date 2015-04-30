from wq.io.base import *
from wq.io.loaders import *
from wq.io.parsers import *
from wq.io.mappers import *
from wq.io.util import make_io, load_file, load_string, guess_type, flattened
from wq.io.version import VERSION

# Some useful pre-mixed classes
CsvFileIO = make_io(FileLoader, CsvParser)
CsvNetIO = make_io(NetLoader, CsvParser)
CsvStringIO = make_io(StringLoader, CsvParser)

JsonFileIO = make_io(FileLoader, JsonParser)
JsonNetIO = make_io(NetLoader, JsonParser)
JsonStringIO = make_io(StringLoader, JsonParser)

XmlFileIO = make_io(BinaryFileLoader, XmlParser, name='XmlFileIO')
XmlNetIO = make_io(NetLoader, XmlParser)
XmlStringIO = make_io(StringLoader, XmlParser)

ExcelFileIO = make_io(BinaryFileLoader, ExcelParser, name='ExcelFileIO')

try:
    import fiona
    import shapely
    from wq.io.gis import GisIO, ShapeIO, WktIO
except ImportError:
    pass
