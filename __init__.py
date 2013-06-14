from wq.io.base    import *
from wq.io.loaders import *
from wq.io.parsers import *
from wq.io.mappers import *
from wq.io.util    import make_io, load_file, guess_type

# Some useful pre-mixed classes
CsvFileIO   = make_io(FileLoader,       CsvParser)
CsvNetIO    = make_io(NetLoader,        CsvParser)
JsonFileIO  = make_io(FileLoader,       JsonParser)
JsonNetIO   = make_io(NetLoader,        JsonParser)
XmlFileIO   = make_io(FileLoader,       XmlParser)
XmlNetIO    = make_io(NetLoader,        XmlParser)
ExcelFileIO = make_io(BinaryFileLoader, ExcelParser, name='ExcelFileIO')
