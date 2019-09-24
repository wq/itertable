try:
    import unicodecsv as csv
    UNICODE_CSV = True
except ImportError:
    import csv
    UNICODE_CSV = False


if issubclass(csv.DictReader, object):
    # Python 3
    DictReader = csv.DictReader
else:
    # Python 2
    class DictReader(object, csv.DictReader):
        pass


class SkipPreludeReader(DictReader):
    """
    A specialized version of DictReader that attempts to find where the "real"
    CSV data is in a file that may contain a prelude of non-CSV text.
    """

    max_header_row = 20

    def __init__(self, f, fieldnames=None, restkey=None, restval=None,
                 dialect="excel", *args, **kwds):
        # Preserve file since we're going to start reading it
        self._file = f

        # Preserve reader options since we'll need to make another one
        readeropts = [f, dialect]
        readeropts.extend(args)
        self._readeropts = (readeropts, kwds)
        csv.DictReader.__init__(self, f, fieldnames, restkey, restval,
                                dialect, *args, **kwds)

    @property
    def fieldnames(self):
        if self._fieldnames is not None:
            return self._fieldnames

        # Create a new reader just to figure out which row is the header
        args, kwds = self._readeropts
        data = csv.reader(*args, **kwds)
        rows = []
        for i in range(self.max_header_row):
            try:
                rows.append(next(data))
            except StopIteration:
                pass
        header_row, field_names = self.choose_header(rows)

        # Reset file and advance reader so it starts in the right spot
        self._file.seek(0)
        for i in range(header_row + 1):
            try:
                next(self.reader)
            except StopIteration:
                pass

        self._fieldnames = field_names
        self._header_row = header_row
        return field_names

    @property
    def header_row(self):
        self.fieldnames  # used for side effect
        return self._header_row

    def choose_header(self, rows):
        """
        Determine which row contains column headers from the provided set.
        Default is to assume that the first longest row is the header.
        """
        header_row = 0
        field_names = []

        # Select header from available rows
        for i, row in enumerate(rows):
            if len(row) > len(field_names):
                header_row = i
                field_names = row
        return header_row, field_names
