from wq.io.base import BaseIO

class IOCollectionItem(BaseIO):
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

class IOCollection(BaseIO):
    "An IO that itself contains IO objects"

    item_class = IOCollectionItem
    item_field_names = None

    def usable_item(self, item):
        return self.item_class(collection=self, data=item)

    def parse_usable_item(self, item):
        raise NotImplementedError
