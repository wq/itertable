from itertable.gis import ShapeIter
from shapely.geometry import Point
from .base import IterTestCase
from os import unlink


class GisTestCase(IterTestCase):
    def setUp(self):
        self.points = [
            Point(-93.278, 44.976),
            Point(-93.247, 44.973),
        ]
        self.types = ('geojson', 'shp',)

    def test_shapeio(self):
        for ext in self.types:
            filename = self.get_filename("test", ext)
            instance = ShapeIter(filename=filename)
            self.check_instance(instance)

    def test_shapeio_sync(self):
        for source_ext in self.types:
            for dest_ext in self.types:
                source_file = self.get_filename("test", source_ext)
                dest_file = self.get_filename("sync", dest_ext, True)
                source_instance = ShapeIter(filename=source_file)
                dest_instance = ShapeIter(
                    filename=dest_file, require_existing=False
                )
                source_instance.sync(dest_instance)
                self.check_instance(ShapeIter(filename=dest_file))

    def check_instance(self, instance):
        self.assertEqual(len(instance), len(self.data))

        for row, data, point in zip(instance.values(), self.data, self.points):
            for key in data:
                val = getattr(row, key)
                try:
                    val = int(val)
                except ValueError:
                    pass
                self.assertEqual(val, data[key])
                self.assertTrue(row.geometry.contains(point))

    def get_filename(self, filename, ext, remove_existing=False):
        filename = super(GisTestCase, self).get_filename(
            filename, ext, remove_existing
        )
        if ext == 'shp' and remove_existing:
            for ext in ('dbf', 'shx', 'prj'):
                try:
                    unlink(filename.replace('shp', ext))
                except OSError:
                    pass
        return filename
