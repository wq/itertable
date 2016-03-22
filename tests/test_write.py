from wq.io import load_file
import unittest
import pickle
from wq.io import CsvFileIO, JsonFileIO, XmlFileIO, ExcelFileIO
from .base import IoTestCase


class LoadFileTestCase(IoTestCase):
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
        self.types = ('csv', 'json', 'xml', 'xls', 'xlsx')
        self.classes = (
            CsvFileIO,
            JsonFileIO,
            XmlFileIO,
            ExcelFileIO,
            ExcelFileIO,
        )

    def test_write_file(self):
        """
        Test BaseIO.save() when starting from an empty IO instance
        """
        for ext, cls in zip(self.types, self.classes):
            filename = self.get_filename("output", ext, True)

            # Create an empty instance of the class
            instance = cls(
                filename=filename,
                field_names=['one', 'two', 'three'],

                # These only apply to XmlFileIO, will be ignored by the others
                root_tag="root",
                item_tag="item"
            )

            # Add rows to the instance using list-style BaseIO.append()
            for row in self.data:
                instance.append(instance.create(**row))

            # Save the instance, which should write to output.[ext]
            instance.save()

            # The contents of the saved file should match the original data
            self.check_instance(load_file(filename))

    def duplicate(self, mode, xform):
        """
        Test BaseIO.copy/sync() (and implicit save()) between combinations of
        the default IO classes.
        """
        for source_ext, source_cls in zip(self.types, self.classes):
            for dest_ext, dest_cls in zip(self.types, self.classes):
                source_file = self.get_filename("test", source_ext)
                dest_file = self.get_filename(mode, dest_ext, True)

                # Sync requires key_field to be set on both classes
                source_cls = xform(source_cls)
                dest_cls = xform(dest_cls)

                # Load source data into IO instance
                source_instance = source_cls(filename=source_file)

                # Create empty instance of the destination IO class
                dest_instance = dest_cls(
                    filename=dest_file,
                    field_names=['one', 'two', 'three'],
                    root_tag="root",
                    item_tag="item",
                )

                # The Sync
                getattr(source_instance, mode)(dest_instance)

                # Load the destination file again and check contents
                self.check_instance(load_file(dest_file))

    def test_copy_io(self):
        self.duplicate('copy', lambda d: d)

    def test_sync_io(self):
        self.duplicate('sync', self.with_key_field)

    def with_key_field(self, cls):
        class new_class(cls):
            key_field = "one"
        new_class.__name__ = "Dict" + cls.__name__
        return new_class
