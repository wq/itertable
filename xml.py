from wq.io.base import IO
from wq.io.file import FileIO
from wq.io.net  import NetIO

from lxml import etree

class XmlIO(IO):
    "wq.io.XmlIO: load XML documents for use in wq.io"

    itemtag = None

    def load(self):
        root = etree.parse(self.file)
        self.data = root.findall(self.itemtag)

    @property
    def field_names(self):
        "Attempt to infer field names from first item in XML"
        if not self.data:
            raise NotImplementedError
        return [e.tag for e in self.data[0]]

    def totuple(self, el):
        d = {e.tag: e.text for e in el}
        return super(XmlIO, self).totuple(d)

    def fromtuple(self, item):
        el = etree.Element(self.itemtag)
        for k in self.field_name_map:
            if getattr(item, k) is None:
                continue
            sel = etree.SubElement(el, self.field_name_map[k])
            sel.text = unicode(getattr(item, k))
        return el

class XmlFileIO(FileIO, XmlIO):
    pass

class XmlNetIO(NetIO, XmlIO):
    pass
