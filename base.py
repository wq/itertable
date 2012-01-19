from collections import MutableMapping, MutableSequence

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

    # If load() method creates self.data as a mutable mapped sequence
    # the methods below will automatically work.

    # Otherwise, they should be overridden.

    def __len__(self):
        if not hasattr(self, 'data'):
            raise NotImplementedError
        else:
            return len(self.data)

    def __getitem__(self, key):
        if not hasattr(self, 'data'):
            raise NotImplementedError
        else:
            return self.data[key]

    def __setitem__(self, key, item):
        if not hasattr(self, 'data'):
            raise NotImplementedError
        else:
            self.data[key] = item

    def __delitem__(self, key):
        if not hasattr(self, 'data'):
            raise NotImplementedError
        else:
            del self.data[key]

    def insert(self, item):
        if not hasattr(self, 'data'):
            raise NotImplementedError
        else:
            self.data.insert(key)

    def __iter__(self, key):
        if not hasattr(self, 'data'):
            raise NotImplementedError
        else:
            for item in self.data:
                yield item
