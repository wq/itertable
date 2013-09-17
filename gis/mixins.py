from wq.io.gis.gdal import DataSource, Layer, Feature
from wq.io.loaders import FileLoader
from wq.io.mappers import TupleMapper


class GisLoader(FileLoader):
    def load(self):
        self.datasource = DataSource(self.filename)

    def save(self):
        raise NotImplementedError


class GisParser(object):
    layer = None
    layer_name = None

    def parse(self):
        if len(self.datasource) == 1:
            self.layer_name = self.datasource[0].name

        if self.layer_name is None:
            self.data = [{'name': l.name, 'count': len(l), 'data': l}
                         for l in self.datasource]
            return

        for l in self.datasource:
            if l.name == self.layer_name:
                self.data = map(self.parse_feature, l)
                self.layer = l

    def parse_feature(self, f):
        feat = {key: f.get(key) for key in f.fields}
        feat['geometry'] = f.geom
        return feat

    def dump_feature(self, feat):
        raise NotImplementedError


class WktMapper(TupleMapper):
    def map_value(self, field, value):
        if field == 'geometry':
            return value.wkt
        else:
            return value
