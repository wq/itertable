from wq.io import (
    ZipFileLoader, ZipNetLoader,
    CsvParser, ExcelParser, TupleMapper, BaseIO
)
from .base import IoTestCase
from wq.io.exceptions import LoadFailed
import httpretty


class CsvZipFileIO(ZipFileLoader, CsvParser, TupleMapper, BaseIO):
    inner_binary = CsvParser.binary


class ExcelZipFileIO(ZipFileLoader, ExcelParser, TupleMapper, BaseIO):
    inner_binary = True


class CsvZipNetIO(ZipNetLoader, CsvParser, TupleMapper, BaseIO):
    url = "http://example.com/testcsv.zip"
    inner_binary = CsvParser.binary


class ExcelZipNetIO(ZipNetLoader, ExcelParser, TupleMapper, BaseIO):
    url = "http://example.com/testxls.zip"
    inner_binary = True


class ZipFileTestCase(IoTestCase):
    def test_csv_zip(self):
        filename = self.get_filename("testcsv", "zip")
        instance = CsvZipFileIO(filename=filename)
        self.check_instance(instance)

    def test_xls_zip(self):
        filename = self.get_filename("testxls", "zip")
        instance = ExcelZipFileIO(filename=filename)
        self.check_instance(instance)

    def test_multi_zip(self):
        filename = self.get_filename("testmulti", "zip")
        with self.assertRaises(LoadFailed) as cm:
            instance = CsvZipFileIO(filename=filename)
        self.assertEqual(str(cm.exception), "Multiple Inner Files!")

    def test_multi_zip_name(self):
        filename = self.get_filename("testmulti", "zip")
        instance = CsvZipFileIO(filename=filename, inner_filename="test.csv")
        self.check_instance(instance)


class NetZipFileTestCase(IoTestCase):
    def setUp(self):
        httpretty.enable()
        self.register_url("testcsv")
        self.register_url("testxls")

    def register_url(self, name):
        filename = self.get_filename(name, "zip")
        zipfile = open(filename, "rb")
        zipdata = zipfile.read()
        zipfile.close()
        httpretty.register_uri(
            httpretty.GET,
            "http://example.com/%s.zip" % name,
            body=zipdata,
            content_type="application/zip"
        )

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def test_load_zip(self):
        self.check_instance(CsvZipNetIO())

    def test_xls_zip(self):
        self.check_instance(ExcelZipNetIO())
