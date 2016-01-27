from collections import MutableMapping, MutableSequence


class BaseIO(MutableMapping, MutableSequence):
    "wq.io.BaseIO: Base class for generic resource management"

    tabular = False
    nested = False
    binary = False

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.refresh()

    def refresh(self):
        self.load()
        if getattr(self, 'empty_file', False):
            self.data = []
        else:
            self.parse()
            if hasattr(self, 'file') and not self.file.closed:
                self.file.close()

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
        file.write(str(self.data))

    def save(self):
        ""
        self.dump(self.file)

    field_names = None
    scan_fields = False
    _auto_field_names = None

    def get_field_names(self):
        "Returns a list of raw fields to expect (defined by parser mixins)"
        if self.field_names is not None:
            # Support specifying field_names as string (like namedtuple does)
            if isinstance(self.field_names, str):
                return self.field_names.replace(',', ' ').split()
            else:
                return self.field_names

        # If no defined field names, try to retrieve from data
        if not getattr(self, 'data', None):
            return None

        if self._auto_field_names:
            return self._auto_field_names

        if self.scan_fields:
            # Scan all rows for field names
            field_names = set()
            for row in self.data:
                field_names.update(row.keys())
            field_names = list(field_names)
        else:
            # Assume first row contains same keys as all other rows
            field_names = list(self.data[0].keys())

        self._auto_field_names = field_names
        return field_names

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

    def compute_index(self, recompute=False):
        key_field = self.get_key_field()
        if key_field is None:
            return None

        if getattr(self, '_index_cache', None) is not None and not recompute:
            return self._index_cache

        index = {}
        for i, item in enumerate(self.data):
            uitem = self.usable_item(item)
            if isinstance(uitem, dict):
                key = uitem.get(key_field, None)
            else:
                key = getattr(uitem, key_field, None)
            if key is not None:
                index[key] = i

        self._index_cache = index
        return index

    def find_index(self, key):
        index = self.compute_index()
        if index is not None:
            return index.get(key, None)
        else:
            return key

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
            self.compute_index(True)

    def __delitem__(self, key):
        index = self.find_index(key)
        if index is None:
            raise KeyError
        del self.data[index]
        self.compute_index(True)

    def insert(self, index, uitem):
        item = self.parse_usable_item(uitem)
        self.data.insert(index, item)
        self.compute_index(True)

    def __iter__(self):
        for item in self.data:
            uitem = self.usable_item(item)
            if uitem is None:
                return
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

    # Slots to track things that can't be pickled
    # (need a separate slot for each expected mixin class, since they don't
    #  extend BaseIO)
    no_pickle = []
    no_pickle_loader = []
    no_pickle_mapper = []
    no_pickle_parser = []

    def get_no_pickle(self):
        return (
            self.no_pickle +
            self.no_pickle_loader +
            self.no_pickle_mapper +
            self.no_pickle_parser
        )

    def __getstate__(self):
        """
        Don't include auto-created and unpicklable properties in state.
        """
        state = self.__dict__.copy()
        for name in self.get_no_pickle():
            state.pop(name, None)
        return state

    def item_dict(self, item):
        return item

    def as_dataframe(self):
        from pandas import DataFrame
        key = self.get_key_field()
        if key:
            data = [self.item_dict(row) for row in self.values()]
        else:
            data = [self.item_dict(row) for row in self]
        df = DataFrame(data)
        if key:
            df.set_index(key, inplace=True)
        return df
