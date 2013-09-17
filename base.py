from collections import MutableMapping, MutableSequence


class BaseIO(MutableMapping, MutableSequence):
    "wq.io.BaseIO: Base class for generic resource management"

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.refresh()

    def refresh(self):
        self.load()
        self.parse()

    def load(self):
        "Open a resource (defined by loader mixins)"
        # self.file = ...
        pass

    def parse(self):
        """
        Parse a resource (defined by parser mixins).
        Result should be an iterable of dicts.
        """
        # self.data = some_parse_method(self.file)
        pass

    def dump(self, file=None):
        ""
        if file is None:
            file = self.file
        file.write(unicode(self.data))

    def save(self):
        ""
        self.dump(self.file)

    field_names = None

    def get_field_names(self):
        "Returns a list of raw fields to expect (defined by parser mixins)"
        if self.field_names is not None:
            #Support specifying field_names as string (like namedtuple does)
            if isinstance(self.field_names, basestring):
                return self.field_names.replace(',', ' ').split()
            else:
                return self.field_names

        # If no defined field names, try to retrieve from first record
        if getattr(self, 'data', None) and len(self.data) > 0:
            return self.data[0].keys()
        else:
            return None

    @property
    def key_field(self):
        "Assign a key_field to use the resource as a Map"
        return None

    def get_key_field(self):
        return self.key_field

    def usable_item(self, item):
        "Hook to allow items to be transformed"
        return item

    def parse_usable_item(self, uitem):
        "Hook to allow items to be untransformed"
        return uitem

    def find_index(self, key):
        pk = self.get_key_field()
        if pk is None:
            return key
        for index, item in enumerate(self.data):
            uitem = self.usable_item(item)
            if isinstance(uitem, dict):
                if uitem.get(pk, None) == key:
                    return index
            else:
                if getattr(uitem, pk, None) == key:
                    return index

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        index = self.find_index(key)
        if index is None:
            raise KeyError
        return self.usable_item(self.data[index])

    def __setitem__(self, key, uitem):
        item = self.parse_usable_item(uitem)
        index = self.find_index(key)
        if index is not None:
            self.data[index] = item
        else:
            self.data.append(item)

    def __delitem__(self, key):
        index = self.find_index(key)
        if index is None:
            raise KeyError
        del self.data[index]

    def insert(self, index, uitem):
        item = self.parse_usable_item(uitem)
        self.data.insert(index, item)

    def __iter__(self):
        for item in self.data:
            uitem = self.usable_item(item)
            pk = self.get_key_field()
            if pk is None:
                yield uitem
            elif isinstance(uitem, dict):
                yield uitem.get(pk, None)
            else:
                yield getattr(uitem, pk, None)

    def sync(self, other, save=True):
        if self.get_key_field() is None or other.get_key_field() is None:
            raise Exception("Key field required to sync!")
        for key in self:
            other[key] = self[key]
        if save:
            other.save()

    def copy(self, other, save=True):
        del other.data[:]
        for item in self.data:
            uitem = self.usable_item(item)
            other.append(uitem)
        if save:
            other.save()
