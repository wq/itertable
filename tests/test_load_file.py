from itertable import load_file
from itertable.exceptions import NoData
from .base import IterTestCase
import pickle


class LoadFileTestCase(IterTestCase):
    def setUp(self):
        self.types = ('csv', 'json', 'xml', 'xls', 'xlsx')

    def test_load_file(self):
        for ext in self.types:
            filename = self.get_filename("test", ext)
            instance = load_file(filename)
            self.check_instance(instance)

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
