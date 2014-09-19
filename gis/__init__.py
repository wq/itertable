from .mixins import FionaLoaderParser, GisMapper, ShapeMapper, WktMapper
from wq.io.base import BaseIO


class MetaSyncIO(BaseIO):
    """
    Custom sync() to handle transfering Fiona metadata (except for driver)
    """
    def sync(self, other, save=True):
        driver = other.meta.get('driver', None)
        other.meta = self.meta.copy()
        if driver:
            other.meta['driver'] = driver
        super(MetaSyncIO, self).sync(other, save)

    def get_field_names(self):
        if self.field_names is None and self.meta is not None:
            return (
                ['id', 'geometry']
                + list(self.meta['schema']['properties'].keys())
            )
        return super(MetaSyncIO, self).get_field_names()


class GisIO(FionaLoaderParser, GisMapper, MetaSyncIO):
    pass


class ShapeIO(FionaLoaderParser, ShapeMapper, MetaSyncIO):
    pass


class WktIO(FionaLoaderParser, WktMapper, MetaSyncIO):
    pass
