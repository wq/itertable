from wq.io.mappers import TupleMapper
from wq.io.gis.mixins import GisParser, GisLoader, WktMapper
from wq.io.base import BaseIO


class GisIO(GisLoader, GisParser, TupleMapper, BaseIO):
    pass


class WktIO(GisLoader, GisParser, WktMapper, BaseIO):
    pass
