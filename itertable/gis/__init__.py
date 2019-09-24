from .mixins import FionaLoaderParser, GisMapper, ShapeMapper, WktMapper
from ..base import BaseIter


class MetaSyncIter(BaseIter):
    """
    Custom sync() to handle transfering Fiona metadata (except for driver)
    """
    def sync(self, other, save=True):
        driver = other.meta.get('driver', None)
        other.meta = self.meta.copy()
        if driver:
            other.meta['driver'] = driver
        super(MetaSyncIter, self).sync(other, save)

    def get_field_names(self):
        if self.field_names is None and self.meta is not None:
            return (
                ['id', 'geometry']
                + list(self.meta['schema']['properties'].keys())
            )
        return super(MetaSyncIter, self).get_field_names()


class GisIter(FionaLoaderParser, GisMapper, MetaSyncIter):
    pass


class ShapeIter(FionaLoaderParser, ShapeMapper, MetaSyncIter):
    pass


class WktIter(FionaLoaderParser, WktMapper, MetaSyncIter):
    pass
