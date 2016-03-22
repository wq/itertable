import json
from .readers import csv, UNICODE_CSV, SkipPreludeReader
from xml.etree import ElementTree as ET

from .base import BaseParser, TableParser
from wq.io.exceptions import ParseFailed


class CsvParser(TableParser):
    delimiter = ","
    quotechar = '"'
    no_pickle_parser = ['csvdata']
    binary = UNICODE_CSV

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

        Reader = self.reader_class()
        self.csvdata = Reader(
            self.file,
            fields,
            delimiter=self.delimiter,
            quotechar=self.quotechar,
        )
        self.field_names = self.csvdata.fieldnames
        if self.header_row is not None:
            self.header_row = self.csvdata.header_row
        self.data = [row for row in self.csvdata]
        self.extra_data = {}

    def reader_class(self):
        class Reader(SkipPreludeReader):
            max_header_row = self.max_header_row
        return Reader

    def dump(self, file=None):
        if file is None:
            file = self.file
        args = file, self.get_field_names()
        kwargs = {'encoding': 'utf-8'} if UNICODE_CSV else {}
        kwargs['delimiter'] = self.delimiter
        kwargs['quotechar'] = self.quotechar
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
            self.data = list(map(self.parse_item, obj))
        except ValueError:
            raise ParseFailed

    def parse_item(self, item):
        return item

    def dump(self, file=None):
        if file is None:
            file = self.file
        obj = list(map(self.dump_item, self.data))
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
        doc = ET.parse(self.file)
        root = self.parse_root(doc)
        if self.root_tag is None:
            self.root_tag = root.tag
        if self.item_tag is None:
            self.item_tag = list(root)[0].tag
        self.data = list(map(self.parse_item, root.findall(self.item_tag)))

    def parse_root(self, doc):
        root = doc.getroot()
        if self.root_tag is not None and root.tag != self.root_tag:
            root = root.find(self.root_tag)
        return root

    def parse_item(self, el):
        return {e.tag: e.text for e in el}

    def dump(self, file=None):
        if file is None:
            file = self.file
        root = ET.Element(self.root_tag)
        for item in self.data:
            root.append(self.dump_item(item))
        output = ET.tostring(root).decode('utf-8')
        file.write(output)

    def dump_item(self, item):
        el = ET.Element(self.item_tag)
        for key in self.get_field_names():
            if key not in item or item[key] is None:
                continue
            sel = ET.SubElement(el, key)
            sel.text = str(item.get(key))
        return el
