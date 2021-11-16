from os.path import join, dirname
from os import unlink
import unittest


class IterTestCase(unittest.TestCase):
    data = [{
        'one': 1,
        'two': 2,
        'three': 3,
    }, {
        'one': 4,
        'two': 5,
        'three': 6,
    }]

    def get_filename(self, filename, ext, remove_existing=False):
        filename = join(dirname(__file__), "files", "%s.%s" % (filename, ext))
        if remove_existing:
            try:
                unlink(filename)
            except OSError:
                pass
        return filename

    def check_instance(self, instance):
        self.assertEqual(len(instance), len(self.data))

        for row, data in zip(instance, self.data):
            for key in data:
                val = getattr(row, key)
                try:
                    val = int(float(val))
                except ValueError:
                    pass
                self.assertEqual(val, data[key])
