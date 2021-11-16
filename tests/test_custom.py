from itertable import JsonFileIter, XmlFileIter
from itertable.exceptions import MappingFailed
from .base import IterTestCase


class CustomJsonFileIter(JsonFileIter):
    namespace = "data.items"


class ExtraJsonFileIter(CustomJsonFileIter):
    scan_fields = True


class CustomXmlFileIter(XmlFileIter):
    root_tag = "items"
    item_tag = "item"


class CustomTestCase(IterTestCase):
    def test_custom_json(self):
        filename = self.get_filename("custom", "json")
        instance = CustomJsonFileIter(filename=filename)
        self.check_instance(instance)

    def test_scan_fields(self):
        filename = self.get_filename("custom2", "json")
        instance = ExtraJsonFileIter(filename=filename)
        self.check_instance(instance)
        self.assertIn("four", instance.get_field_names())
        self.assertIsNone(instance[0].four)
        self.assertEqual(instance[1].four, "extra")

    def test_unexpected_field(self):
        filename = self.get_filename("custom2", "json")
        instance = CustomJsonFileIter(filename=filename)
        # Extra field in non-first row breaks namedtuple
        with self.assertRaises(MappingFailed) as e:
            instance[1]
        self.assertIn("unexpected field", str(e.exception))

    def test_custom_xml(self):
        filename = self.get_filename("custom", "xml")
        instance = CustomXmlFileIter(filename=filename)
        self.check_instance(instance)
