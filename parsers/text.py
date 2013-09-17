import json

try:
    import unicodecsv as csv
    UNICODE_CSV = True
except ImportError:
    import csv
    UNICODE_CSV = False

from lxml import etree as xml

from .base import BaseParser, TableParser


class CsvParser(TableParser):

    def parse(self):
        # Like DictReader, assume explicit field definition means CSV does not
        # contain column headers.
        fields = self.get_field_names()
        if self.start_row is None:
            if fields:
                self.start_row = 0
            else:
                self.start_row = 1
        if self.header_row is None:
            if fields:
                self.header_row = None
            else:
                self.header_row = 0

        self.csvdata = csv.DictReader(self.file, fields)
        self.field_names = self.csvdata.fieldnames
        self.data = [row for row in self.csvdata]

    def dump(self, file=None):
        if file is None:
            file = self.file
        args = file, self.get_field_names()
        kwargs = {'encoding': 'utf-8'} if UNICODE_CSV else {}
        csvout = csv.DictWriter(*args, **kwargs)
        csvout.writeheader()
        for row in self.data:
            csvout.writerow(row)


class JsonParser(BaseParser):
    indent = None
    namespace = None

    def parse(self):
        try:
            obj = json.load(self.file)
            if self.namespace:
                for key in self.namespace.split('.'):
                    obj = obj[key]
            self.data = map(self.parse_item, obj)
        except ValueError:
            self.data = []

    def parse_item(self, item):
        return item

    def dump(self, file=None):
        if file is None:
            file = self.file
        obj = map(self.dump_item, self.data)
        if self.namespace:
            for key in reversed(self.namespace.split('.')):
                obj = {key: obj}
        json.dump(obj, file, indent=self.indent)

    def dump_item(self, item):
        return item


class XmlParser(BaseParser):
    root_tag = None
    item_tag = None

    def parse(self):
        doc = xml.parse(self.file)
        root = doc.getroot()
        if self.root_tag is None:
            self.root_tag = root.tag
        if self.item_tag is None:
            self.item_tag = list(root)[0].tag
        self.data = map(self.parse_item, root.findall(self.item_tag))

    def parse_item(self, el):
        return {e.tag: e.text for e in el}

    def dump(self, file=None):
        if file is None:
            file = self.file
        root = xml.Element(self.root_tag)
        for item in self.data:
            root.append(self.dump_item(item))
        xml.ElementTree(root).write(file)

    def dump_item(self, item):
        el = xml.Element(self.item_tag)
        for key in self.get_field_names():
            if key not in item or item[key] is None:
                continue
            sel = xml.SubElement(el, key)
            sel.text = unicode(item.get(key))
        return el
