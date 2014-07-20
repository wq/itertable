from os.path import join, dirname
from os import unlink
import unittest


class IoTestCase(unittest.TestCase):
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
