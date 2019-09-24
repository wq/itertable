from itertable import ExcelFileIter
from .base import IoTestCase
from datetime import date


class ExtraDataIter(ExcelFileIter):
    start_row = 5


class LoadFileTestCase(IoTestCase):
    def test_extra_data(self):
        filename = self.get_filename("extra", "xls")
        instance = ExtraDataIter(filename=filename)
        self.check_instance(instance)

        self.assertEqual(instance.extra_data[0][0], "Name")
        self.assertEqual(instance.extra_data[0][1], "Test")
        self.assertEqual(instance.extra_data[1][0], "Type")
        self.assertEqual(instance.extra_data[1][1], "Test")
        self.assertEqual(instance.extra_data[0][3], "Date")
        self.assertEqual(instance.extra_data[0][4], date(2014, 12, 12))

    def test_no_extra_data(self):
        filename = self.get_filename("extra", "xls")
        ExtraDataIter(filename=filename)
        filename = self.get_filename("noextra", "xls")
        instance = ExtraDataIter(filename=filename)
        self.check_instance(instance)
        self.assertFalse(instance.extra_data)

    def check_instance(self, instance):
        self.assertEqual(len(instance), len(self.data))

        for row, data in zip(instance, self.data):
            for key in data:
                val = getattr(row, key)
                if isinstance(val, str) and val.isdigit():
                    val = int(val)
                self.assertEqual(val, data[key])
