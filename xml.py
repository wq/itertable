from wq.io.base import IO
from lxml import etree

class XmlIO(IO):
    "wq.io.XmlIO: load XML documents for use in wq.io"

    xml = None

    def load(self):
        self.xml = etree.parse(self.file)

    @property
    def itemtag(self):
        raise NotImplementedError
    
    @property
    def itemkey(self):
        return None
    
    @property
    def root(self):
        return self.xml.getroot()

    @property
    def itemlist(self):
        return self.root.findall(self.itemtag)

    def __len__(self):
        return len(self.itemlist)

    def __iter__(self):
        for el in self.itemlist:
            yield self.todict(el)

    def __getitem__(self, key):
        if self.itemkey is None:
            return self.todict(self.itemlist[key])

        for item in self:
            if item[self.itemkey] == key:
                return item
    
    def __setitem__(self, key, item):
        raise NotImplementedError
    
    def __delitem__(self, key, item):
        raise NotImplementedError

    def append(self, item):
        if self.itemkey is not None and self.itemkey not in item:
            item[self.itemkey] = self.generatekey(item)
        self.root.append(self.toxml(item))

    def todict(self, el):
        return {e.tag: e.text for e in el}

    def toxml(self, item):
        el = etree.Element(self.itemtag)
        for k, v in item.iteritems():
            sel = etree.SubElement(el, k)
            sel.text = v
        return el

    def generatekey(self, item):
        raise NotImplementedError
