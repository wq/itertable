from itertable import load_file
from itertable.exceptions import LoadFailed, NoData
from .base import IterTestCase
import unittest
import pickle
import io

try:
    import magic
except ImportError:
    magic = None


class LoadFileTestCase(IterTestCase):
    def setUp(self):
        self.types = ('csv', 'json', 'xml', 'xls', 'xlsx')

    def test_load_file(self):
        for ext in self.types:
            filename = self.get_filename("test", ext)
            instance = load_file(filename)
            self.check_instance(instance)

    def test_load_file_object(self):
        for ext in self.types:
            filename = self.get_filename("test", ext)
            if ext in ('xls', 'xlsx'):
                mode = 'rb'
            else:
                mode = 'r'
            with open(filename, mode) as f:
                instance = load_file(f)
            self.check_instance(instance)

    def test_load_file_object_binary(self):
        for ext in self.types:
            filename = self.get_filename("test", ext)
            with open(filename, 'rb') as f:
                instance = load_file(f)
            self.check_instance(instance)

    @unittest.skipUnless(magic, "magic required for buffer-based detection")
    def test_load_file_object_no_name(self):
        for ext in self.types:
            filename = self.get_filename("test", ext)
            if ext in ('xls', 'xlsx'):
                mode = 'rb'
                IO = io.BytesIO
            else:
                mode = 'r'
                IO = io.StringIO

            with open(filename, mode) as f:
                obj = IO(f.read())

            instance = load_file(obj)
            self.check_instance(instance)

    def test_load_file_like(self):
        class FileLike:
            name = "test.csv"

            def read(self, *args, **kwargs):
                return "one,two,three\n1,2,3\n4,5,6"

            def __iter__(self):
                yield from self.read().split('\n')

        instance = load_file(FileLike())
        self.check_instance(instance)

    def test_load_non_file(self):
        with self.assertRaises(AssertionError):
            load_file([{"value": "not a file"}])

    def test_load_csv_prelude(self):
        filename = self.get_filename("test2", "csv")
        instance = load_file(filename)
        self.check_instance(instance)

    def test_load_csv_unicode(self):
        filename = self.get_filename("test3", "csv")
        instance = load_file(filename)
        self.check_instance(instance)
        self.assertTrue(hasattr(instance[0], "μ"))
        self.assertEqual(instance[0].μ, "test")

    def test_load_xlsx_sheets(self):
        filename = self.get_filename("test", "xlsx")
        instance = load_file(filename, options={'sheet_name': None})
        self.assertEqual(len(instance), 1)
        self.assertEqual(instance[0].name, 'Sheet1')
        self.check_instance(instance[0].data)

    def test_load_nodata(self):
        filename = self.get_filename("nodata", "csv")
        instance = load_file(filename)
        with self.assertRaises(NoData) as cm:
            instance[0]
        self.assertEqual(str(cm.exception), "No data returned!")

    def test_load_nodata_excel(self):
        filename = self.get_filename("nodata", "xlsx")
        instance = load_file(filename)
        with self.assertRaises(NoData) as cm:
            instance[0]
        self.assertEqual(str(cm.exception), "No data returned!")

    def test_load_nodata_excel_sheets(self):
        filename = self.get_filename("nodata", "xlsx")
        instance = load_file(filename, options={'sheet_name': None})
        self.assertEqual(len(instance), 1)
        self.assertEqual(instance[0].name, 'Sheet1')
        sheet = instance[0].data
        with self.assertRaises(NoData) as cm:
            sheet[0]
        self.assertEqual(str(cm.exception), "No data returned!")

    def test_load_non_existing(self):
        filename = self.get_filename("nonexisting", "csv")
        with self.assertRaises(LoadFailed) as cm:
            load_file(filename)
        self.assertEqual(str(cm.exception), "No such file or directory")

    def test_load_init_empty(self):
        filename = self.get_filename("nonexisting", "csv")
        instance = load_file(filename, options={'require_existing': False})
        with self.assertRaises(NoData) as cm:
            instance[0]
        self.assertEqual(str(cm.exception), "No data returned!")

    def test_pickle(self):
        for ext in self.types:
            filename = self.get_filename("test", ext)
            instance = load_file(filename)
            instance = pickle.loads(pickle.dumps(instance))
            self.check_instance(instance)

    def test_auto_pickle(self):
        for ext in self.types:
            filename = self.get_filename("test", ext)
            instance = load_file(filename)
            # Run through the io once to ensure auto-generated data is present
            self.check_instance(instance)
            instance = pickle.loads(pickle.dumps(instance))
            self.check_instance(instance)
