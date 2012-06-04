from wq.io.base    import BaseIO
from wq.io.loaders import FileLoader, BinaryFileLoader, NetLoader
from wq.io.parsers import CsvParser, JsonParser, XmlParser, ExcelParser
from wq.io.mappers import TupleMapper

# Some useful pre-mixed classes
class TupleIO(TupleMapper, BaseIO):
    pass

class CsvFileIO(FileLoader, CsvParser, TupleIO):
    pass

class CsvNetIO(NetLoader, CsvParser, TupleIO):
    pass

class JsonFileIO(FileLoader, JsonParser, TupleIO):
    pass

class JsonNetIO(NetLoader, JsonParser, TupleIO):
    pass

class XmlFileIO(FileLoader, XmlParser, TupleIO):
    pass

class XmlNetIO(NetLoader, XmlParser, TupleIO):
    pass

class ExcelFileIO(BinaryFileLoader, ExcelParser, TupleIO):
    pass
