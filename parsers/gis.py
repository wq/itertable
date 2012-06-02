from wq.io.base import IOCollection, IOCollectionItem
from wq.io.file import FileIO

from django.contrib.gis.gdal import DataSource

class LayerIO(IOCollectionItem):
    @property
    def field_names(self):
        return self.data.fields + ['geom']

    def totuple(self, feat):
        item = {field: feat.get(name) 
                for field, name in self.field_name_map.items()
                if name != 'geom'}
        item['geom'] = feat.geom
        return self.create_item(**item)

class GisIO(IOCollection):
    item_class = LayerIO
    
    def __iter__(self):
       for layer in self.data:
           yield layer.name

    def __getitem__(self, key):
       for layer in self.data:
           if layer.name == key:
               return self.totuple(layer)
       return KeyError

class GisFileIO(GisIO, FileIO):
    def open(self):
        self.data = DataSource(self.filename)

    def load(self):
        pass
