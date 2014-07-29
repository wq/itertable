from wq.io import load_file
from wq.io.exceptions import NoData
import unittest
from .base import IoTestCase
import pickle


class LoadFileTestCase(IoTestCase):
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

    def check_instance(self, instance):
        self.assertEqual(len(instance), len(self.data))

        for row, data in zip(instance, self.data):
            for key in data:
                val = getattr(row, key)
                if isinstance(val, str) and val.isdigit():
                    val = int(val)
                self.assertEqual(val, data[key])
