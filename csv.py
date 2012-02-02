from __future__ import absolute_import

from wq.io.base import IO
from wq.io.file import FileIO
from wq.io.net  import NetIO

import csv

class CsvIO(IO):
    def load(self):
        self.data = csv.DictReader(self.file)

    @property
    def field_names(self):
        return self.data.fieldnames

class CsvFileIO(FileIO, CsvIO):
    pass

class CsvNetIO(NetIO, CsvIO):
    pass
