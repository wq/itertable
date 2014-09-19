from wq.io.gis import GisIO, WktIO, ShapeIO
from .base import IoTestCase


class GisDataFrameTestCase(IoTestCase):
    def test_gisio_dataframe(self):
        self.dataframe_test(GisIO)

    def test_wktio_dataframe(self):
        self.dataframe_test(WktIO)

    def test_shapeio_dataframe(self):
        self.dataframe_test(ShapeIO)

    def dataframe_test(self, cls):
        instance = cls(filename="tests/files/test.shp")
        df = instance.as_dataframe()
        self.assertEqual(len(df), 2)
        self.assertGreater(df.geometry.area.sum(), 0)
