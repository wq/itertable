from itertable import (
    ZipFileLoader, ZipNetLoader,
    CsvParser, ExcelParser, TupleMapper, BaseIter
)
from .base import IterTestCase
from itertable.exceptions import LoadFailed
import httpretty


class CsvZipFileIter(ZipFileLoader, CsvParser, TupleMapper, BaseIter):
    inner_binary = False


class ExcelZipFileIter(ZipFileLoader, ExcelParser, TupleMapper, BaseIter):
    inner_binary = True


class CsvZipNetIter(ZipNetLoader, CsvParser, TupleMapper, BaseIter):
    url = "http://example.com/testcsv.zip"
    inner_binary = False


class ExcelZipNetIter(ZipNetLoader, ExcelParser, TupleMapper, BaseIter):
    url = "http://example.com/testxlsx.zip"
    inner_binary = True


class ZipFileTestCase(IterTestCase):
    def test_csv_zip(self):
        filename = self.get_filename("testcsv", "zip")
        instance = CsvZipFileIter(filename=filename)
        self.check_instance(instance)

    def test_xlsx_zip(self):
        filename = self.get_filename("testxlsx", "zip")
        instance = ExcelZipFileIter(filename=filename)
        self.check_instance(instance)

    def test_multi_zip(self):
        filename = self.get_filename("testmulti", "zip")
        with self.assertRaises(LoadFailed) as cm:
            CsvZipFileIter(filename=filename)
        self.assertEqual(str(cm.exception), "Multiple Inner Files!")

    def test_multi_zip_name(self):
        filename = self.get_filename("testmulti", "zip")
        instance = CsvZipFileIter(filename=filename, inner_filename="test.csv")
        self.check_instance(instance)


class NetZipFileTestCase(IterTestCase):
    def setUp(self):
        httpretty.enable()
        self.register_url("testcsv")
        self.register_url("testxlsx")

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
        self.check_instance(CsvZipNetIter())

    def test_xlsx_zip(self):
        self.check_instance(ExcelZipNetIter())
