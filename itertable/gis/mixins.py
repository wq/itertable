import fiona
from shapely import wkt, geometry
from ..loaders import FileLoader
from ..exceptions import LoadFailed
from ..parsers.base import BaseParser
from ..mappers import TupleMapper


class FionaLoaderParser(FileLoader, BaseParser):
    """
    Composite loader & parser mixin for GIS data, powered by Fiona
    """
    layer_id = None
    meta = {}
    key_field = 'id'

    def load(self):
        try:
            self.layers = fiona.listlayers(self.filename)
        except OSError as e:
            if self.require_existing:
                raise LoadFailed(
                    e.strerror,
                    path=self.filename,
                    code=e.errno,
                )
            else:
                self.empty_file = True
        except ValueError as e:
            if self.require_existing:
                raise LoadFailed(str(e))
            else:
                self.empty_file = True

        if self.empty_file:
            driver = guess_driver(self.filename)
            self.meta = {'driver': driver}
            self.empty_file = True

    def parse(self):
        # If multiple layers, parse all of them (!)
        if len(self.layers) > 1 and self.layer_id is None:
            cls = type(self)
            self.data = [{
                'id': id,
                'name': name,
                'data': cls(filename=self.filename, layer_id=id)
            } for id, name in enumerate(self.layers)]
        else:
            # One layer, load & parse GIS data
            with fiona.open(self.filename, layer=self.layer_id) as f:
                self.meta = f.meta
                if 'id' in f.meta.get('schema', {}).get('properties', {}):
                    # TODO: Is this correct?
                    del f.meta['schema']['properties']['id']
                self.data = list(map(self.parse_feature, f))

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


class GisMapper(TupleMapper):
    """
    GIS-aware tuple mapper
    """
    def as_dataframe(self):
        # Mimic BaseIter.as_dataframe() but with GeoDataFrame
        # (also, key_field is always set)
        from geopandas import GeoDataFrame
        key = self.get_key_field()
        data = [self.item_dict(row) for row in self.values()]
        df = GeoDataFrame(data)
        df.set_index(key, inplace=True)
        return df

    def item_dict(self, uitem):
        # Turn usable item into GeoDataFrame-friendly dict
        data = uitem._asdict()
        data['geometry'] = geometry.shape(data['geometry'])
        return data


class ShapeMapper(GisMapper):
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

    def item_dict(self, uitem):
        return uitem._asdict()


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

    def item_dict(self, uitem):
        data = uitem._asdict()
        data['geometry'] = wkt.loads(data['geometry'])
        return data


def guess_driver(filename):
    if filename.endswith(".shp"):
        return "ESRI Shapefile"
    else:
        return "GeoJSON"
