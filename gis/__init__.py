from wq.io.mappers import TupleMapper
from .mixins import FionaLoaderParser, ShapeMapper, WktMapper, MetaSyncer
from wq.io.base import BaseIO


class GisIO(FionaLoaderParser, TupleMapper, MetaSyncer, BaseIO):
    pass


class ShapeIO(FionaLoaderParser, ShapeMapper, MetaSyncer, BaseIO):
    pass


class WktIO(FionaLoaderParser, WktMapper, MetaSyncer, BaseIO):
    pass
