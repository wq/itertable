from wq.io import JsonFileIO, XmlFileIO
from wq.io.exceptions import MappingFailed
from .base import IoTestCase


class CustomJsonFileIO(JsonFileIO):
    namespace = "data.items"


class ExtraJsonFileIO(CustomJsonFileIO):
    scan_fields = True


class CustomXmlFileIO(XmlFileIO):
    root_tag = "items"
    item_tag = "item"


class CustomTestCase(IoTestCase):
    def test_custom_json(self):
        filename = self.get_filename("custom", "json")
        instance = CustomJsonFileIO(filename=filename)
        self.check_instance(instance)

    def test_scan_fields(self):
        filename = self.get_filename("custom2", "json")
        instance = ExtraJsonFileIO(filename=filename)
        self.check_instance(instance)
        self.assertIn("four", instance.get_field_names())
        self.assertIsNone(instance[0].four)
        self.assertEqual(instance[1].four, "extra")

    def test_unexpected_field(self):
        filename = self.get_filename("custom2", "json")
        instance = CustomJsonFileIO(filename=filename)
        # Extra field in non-first row breaks namedtuple
        with self.assertRaises(MappingFailed) as e:
            instance[1]
        self.assertIn("unexpected field", str(e.exception))

    def test_custom_xml(self):
        filename = self.get_filename("custom", "xml")
        instance = CustomXmlFileIO(filename=filename)
        self.check_instance(instance)
