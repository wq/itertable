from wq.io import load_file
import unittest
from os.path import dirname, join


class TestLoadFile(unittest.TestCase):
    def setUp(self):
        self.data = [{
            'one': 1,
            'two': 2,
            'three': 3,
        }, {
            'one': 4,
            'two': 5,
            'three': 6,
        }]
        self.types = ('csv', 'json', 'xml', 'xls', 'xlsx')

    def test_load_file(self):
        for ext in self.types:
            filename = join(dirname(__file__), "test.%s" % ext)
            instance = load_file(filename)

            self.assertEqual(len(instance), len(self.data))

            for row, data in zip(instance, self.data):
                for key in data:
                    val = getattr(row, key)
                    if isinstance(val, str) and val.isdigit():
                        val = int(val)
                    self.assertEqual(val, data[key])
