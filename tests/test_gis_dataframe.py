from itertable.gis import GisIter, WktIter, ShapeIter
from .base import IterTestCase


class GisDataFrameTestCase(IterTestCase):
    def test_gisio_dataframe(self):
        self.dataframe_test(GisIter)

    def test_wktio_dataframe(self):
        self.dataframe_test(WktIter)

    def test_shapeio_dataframe(self):
        self.dataframe_test(ShapeIter)

    def dataframe_test(self, cls):
        instance = cls(filename="tests/files/test.shp")
        df = instance.as_dataframe()
        self.assertEqual(len(df), 2)
        self.assertGreater(df.geometry.area.sum(), 0)
