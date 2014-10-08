from wq.io import JsonFileIO, XmlFileIO
from .base import IoTestCase


class CustomJsonFileIO(JsonFileIO):
    namespace = "data.items"


class CustomXmlFileIO(XmlFileIO):
    root_tag = "items"
    item_tag = "item"


class CustomTestCase(IoTestCase):
    def test_custom_json(self):
        filename = self.get_filename("custom", "json")
        instance = CustomJsonFileIO(filename=filename)
        self.check_instance(instance)

    def test_custom_xml(self):
        filename = self.get_filename("custom", "xml")
        instance = CustomXmlFileIO(filename=filename)
        self.check_instance(instance)

    def check_instance(self, instance):
        self.assertEqual(len(instance), len(self.data))

        for row, data in zip(instance, self.data):
            for key in data:
                val = getattr(row, key)
                if isinstance(val, str) and val.isdigit():
                    val = int(val)
                self.assertEqual(val, data[key])
