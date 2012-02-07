from collections import MutableMapping, MutableSequence, namedtuple, OrderedDict
import re

class IO(MutableMapping, MutableSequence):
    "wq.io.IO: Base class for generic resource management"

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.refresh()

    def refresh(self):
        self.open()
        self.load()

    def open(self):
        "Open a resource (overridden by e.g. NetIO)"
        # self.file = ...
        raise NotImplementedError

    def load(self):
        "Parse a resource (overridden by e.g. XmlIO)"
        # self.data = some_parse_method(self.file)
        raise NotImplementedError

    @property
    def field_names(self):
        "Returns a list of fields to expect for individual items"
        raise NotImplementedError

    @property
    def key_field(self):
        "Assign a key_field to use the resource as a Map"
        return None

    @property
    def field_name_map(self):
        #FIXME: check for duplicates
        if not hasattr(self, '_field_name_map'):
            field_names = self.field_names
            #Support specifying field_names as string (like namedtuple does)
            if isinstance(field_names, basestring):
                field_names = field_names.replace(',',' ').split()
            items = [(re.sub(r'\W', '', field.lower()), field) for field in field_names]
            self._field_name_map = OrderedDict(items)
        return self._field_name_map

    @property
    def item_class(self):
        "Returns a class to use for individual items"

        if not hasattr(self, '_item_class'):
           cls = namedtuple(self.__class__.__name__ + 'Item', self.field_name_map.keys())
           self._item_class = cls

        return self._item_class

    @property
    def item_prototype(self):
        if not hasattr(self, '_item_prototype'):
            vals = {field: None for field in self.field_name_map}
            self._item_prototype = self.item_class(**vals)
        return self._item_prototype

    def create_item(self, **kwargs):
        return self.item_prototype._replace(**kwargs)

    # Default implementations of to/fromtuple assume self.data contains dict-like objects
    def totuple(self, item):
        "Convert a single record from the data source to an item_class object"
        mitem = { field: item[name] 
                  for field, name in self.field_name_map.items() 
                  if name in item }
        return self.create_item(**mitem)

    def fromtuple(self, t):
        "Convert a single record from the item_class object to the data source format"
        return {self.field_name_map[key]: getattr(t, key) for key in self.field_name_map}
    
    def generate_key(self, t):
        "Create a key for an item without one"
        raise NotImplementedError

    # Default implementation of collection methods assume
    # self.data is a sequence containing dict-like objects

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        if self.key_field is None:
           return self.totuple(self.data[key])
        else:
           for item in self.data:
               t = self.totuple(item)
               if getattr(t, self.key_field) == key:
                   return t
        return KeyError

    def __setitem__(self, key, t):
        if self.key_field is None:
            self.data[key] = self.fromtuple(t)
        else:
            raise NotImplementedError

    def __delitem__(self, key):
        if self.key_field is None:
            del self.data[key]
        else:
            raise NotImplementedError

    def insert(self, t):
        if self.key_field is not None and not hasattr(t, self.key_field):
            setattr(t, self.key_field, self.generate_key(t))
        self.data.append(self.fromtuple(t))

    def __iter__(self):
        for item in self.data:
            t = self.totuple(item)
            if self.key_field is None:
                yield t
            else:
                yield getattr(t, self.key_field)

class IOCollectionItem(IO):
    "An IO that must be accessed as a member of an IOCollection"
    collection = None

    # Parent collection handles open/load by directly setting data
    def open(self):
        pass

    def load(self):
        pass

    @property
    def field_names(self):
        return self.collection.item_field_names

class IOCollection(IO):
    "An IO that itself contains IO objects"

    item_class = IOCollectionItem
    item_field_names = None

    def totuple(self, item):
        return self.item_class(collection=self, data=item)

    def fromtuple(self, item):
        raise NotImplementedError
