from wq.io.gis import ShapeIO
import unittest
from os.path import dirname, join
import pickle
from shapely.geometry import Point


class GisTestCase(unittest.TestCase):
    def setUp(self):
        self.data = [{
            'one': 1,
            'two': 2,
            'three': 3,
        }, {
            'one': 4,
            'two': 5,
            'three': 6,
        }]
        self.points = [
            Point(-93.278, 44.976),
            Point(-93.247, 44.973),
        ]
        self.types = ('geojson', 'shp',)

    def test_shapeio(self):
        for ext in self.types:
            filename = join(dirname(__file__), "files", "test.%s" % ext)
            instance = ShapeIO(filename=filename)
            self.check_instance(instance)

    def check_instance(self, instance):
        self.assertEqual(len(instance), len(self.data))

        for row, data, point in zip(instance.values(), self.data, self.points):
            for key in data:
                val = getattr(row, key)
                if isinstance(val, str) and val.isdigit():
                    val = int(val)
                self.assertEqual(val, data[key])
                self.assertTrue(row.geometry.contains(point))
