from wq.io.mappers import TupleMapper
from .mixins import FionaLoaderParser, ShapeMapper, WktMapper
from wq.io.base import BaseIO


class MetaSyncIO(BaseIO):
    """
    Custom sync() to handle transfering Fiona meta
    """
    def sync(self, other, save=True):
        other.meta = self.meta
        super(MetaSyncIO, self).sync(other, save)

    def get_field_names(self):
        if self.field_names is None and self.meta is not None:
            return (
                ['id', 'geometry']
                + self.meta['schema']['properties'].keys()
            )
        return super(MetaSyncIO, self).get_field_names()


class GisIO(FionaLoaderParser, TupleMapper, MetaSyncIO):
    pass


class ShapeIO(FionaLoaderParser, ShapeMapper, MetaSyncIO):
    pass


class WktIO(FionaLoaderParser, WktMapper, MetaSyncIO):
    pass
