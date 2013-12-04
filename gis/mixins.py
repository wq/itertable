import fiona
from shapely import wkt, geometry
from wq.io.loaders import FileLoader
from wq.io.parsers.base import BaseParser
from wq.io.mappers import TupleMapper


class FionaLoaderParser(FileLoader, BaseParser):
    """
    Composite loader & parser mixin for GIS data, powered by Fiona
    """
    layer_id = None
    meta = {}
    key_field = 'id'

    def load(self):
        # Load and parse the dataset at the same time via Fiona
        pass

    def parse(self):
        try:
            layers = fiona.listlayers(self.filename)
        except (ValueError, IOError) as e:
            self.data = []
            return

        # If multiple layers, parse all of them (!)
        if len(layers) > 1 and self.layer_id is None:
            cls = type(self)
            self.data = [{
                'id': id,
                'name': name,
                'data': cls(filename=self.filename, layer_id=id)
            } for id, name in enumerate(layers)]
        else:
            # One layer, load & parse GIS data
            with fiona.open(self.filename, layer=self.layer_id) as f:
                self.meta = f.meta
                self.data = map(self.parse_feature, f)

    def parse_feature(self, f):
        # Flatten Fiona's GeoJSON-style representation into something more
        # amenable to namedtuple-ing
        feat = {key: value for key, value in f['properties'].items()}
        if 'id' not in feat and 'ID' not in feat:
            feat['id'] = f['id']
        feat['geometry'] = f['geometry']
        return feat

    def dump_feature(self, feat, i):
        # Undo aforementioned flattening
        return {
            'id': feat.get('id', feat.get('ID', i)),
            'geometry': feat['geometry'],
            'properties': {
                key: value for key, value in feat.items()
                if key not in ('geometry', 'id',)
            }
        }

    def dump(self):
        # Dump and save the dataset at the same time via Fiona
        pass

    def save(self):
        with fiona.open(self.filename, 'w', **self.meta) as f:
            for i, feat in enumerate(self.data):
                f.write(self.dump_feature(feat, i))


class ShapeMapper(TupleMapper):
    """
    Map Fiona's GeoJSON-style geometries to and from Shapely shapes
    """
    def map_value(self, field, value):
        value = super(ShapeMapper, self).map_value(field, value)
        if field == 'geometry':
            value = geometry.shape(value)
        return value

    def unmap_value(self, field, value):
        if field == 'geometry':
            value = geometry.mapping(value)
        return super(ShapeMapper, self).unmap_value(field, value)


class WktMapper(ShapeMapper):
    """
    Map geometries to and from WKT (good for Django integration)
    """
    def map_value(self, field, value):
        value = super(WktMapper, self).map_value(field, value)
        if field == 'geometry':
            value = wkt.dumps(value)
        return value

    def unmap_value(self, field, value):
        if field == 'geometry':
            value = wkt.loads(value)
        return super(WktMapper, self).unmap_value(field, value)
