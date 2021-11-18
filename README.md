**IterTable** is a Pythonic API for iterating through tabular data formats, including CSV, XLSX, XML, and JSON.

```python
from itertable import load_file

for row in load_file("example.xlsx"):
    print(row.date, row.name)
```

[![Latest PyPI Release](https://img.shields.io/pypi/v/itertable.svg)](https://pypi.org/project/itertable)
[![Release Notes](https://img.shields.io/github/release/wq/itertable.svg)](https://github.com/wq/itertable/releases)
[![License](https://img.shields.io/pypi/l/itertable.svg)](https://github.com/wq/itertable/blob/master/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/wq/itertable.svg)](https://github.com/wq/itertable/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/wq/itertable.svg)](https://github.com/wq/itertable/network)
[![GitHub Issues](https://img.shields.io/github/issues/wq/itertable.svg)](https://github.com/wq/itertable/issues)

[![Tests](https://github.com/wq/itertable/actions/workflows/test.yml/badge.svg)](https://github.com/wq/itertable/actions/workflows/test.yml)
[![Python Support](https://img.shields.io/pypi/pyversions/itertable.svg)](https://pypi.python.org/pypi/itertable)

> **Note:** Prior to version 2.0, IterTable was **wq.io**, a submodule of the [wq framework].  The package has been renamed to avoid confusion with the wq framework website (<https://wq.io>).
Similarly, IterTable's `*IO` classes have been renamed to `*Iter`, as the API is not intended to match that of Python's `StringIO` or other `io` classes.

```diff
- from wq.io import CsvFileIO
- data = CsvFileIO(filename='data.csv')
+ from itertable import CsvFileIter
+ data = CsvFileIter(filename='data.csv')
```

## Getting Started

```bash
# Recommended: create virtual environment
# python3 -m venv venv
# . venv/bin/activate

python3 -m pip install itertable

# GIS support (Fiona & Shapely)
python3 -m pip install itertable[gis]

# Excel 97-2003 (.xls) support
python3 -m pip install itertable[oldexcel]
# (xlsx support is enabled by default)

# Pandas integration
python3 -m pip install itertable[pandas]
```

## Overview

IterTable provides a general purpose API for loading, iterating over, and writing tabular datasets.  The goal is to avoid needing to remember the unique usage of e.g. [csv], [openpyxl], or [xml.etree] every time one needs to work with external data.  Instead, IterTable abstracts these libraries into a consistent interface that works as an [iterable] of [namedtuples].  Whenever possible, the field names for a dataset are automatically determined from the source file, e.g. the column headers in an Excel spreadsheet.

```python
from itertable import ExcelFileIter
data = ExcelFileIter(filename='example.xlsx')
for row in data:
    print(row.name, row.date)
```

IterTable provides a number of built-in classes like the above, including a `CsvFileIter`, `XmlFileIter`, and `JsonFileIter`.  There is also a convenience function, `load_file()`, that attempts to automatically determine which class to use for a given file.

```python
from itertable import load_file
data = load_file('example.csv')
for row in data:
    print(row.name, row.date)
```

All of the included `*FileIter` classes support both reading and writing to external files.

### Network Client

IterTable also provides network-capable equivalents of each of the above classes, to facilitate loading data from third party webservices.

```python
from itertable import JsonNetIter
class WebServiceIter(JsonNetIter):
    url = "http://example.com/api"
    
data = WebServiceIter(params={'type': 'all'})
for row in data:
    print(row.timestamp, row.value)
```

The powerful [requests] library is used internally to load data over HTTP.

### Pandas Analysis

When [Pandas] is installed (via `itertable[pandas]`), the `as_dataframe()` method on itertable classes can be used to create a [DataFrame], enabling more extensive analysis possibilities.

```python
instance = WebServiceIter(params={'type': 'all'})
df = instance.as_dataframe()
print(df.value.mean())
```

### GIS Support

When [Fiona] and [Shapely] are installed (via `itertable[gis]`), itertable can also open and create shapefiles and other OGR-compatible geographic data formats.

```python
from itertable import ShapeIter
data = ShapeIter(filename='sites.shp')
for id, site in data.items():
    print(id, site.geometry.wkt)
```

More information on IterTable's gis support is available [here][gis].

### Command-Line Interface

IterTable provides a simple CLI for rendering the content of a file or Iter class.  This can be useful for e.g. inspecting a file or for integrating a shell automation workflow.  The default output is CSV, but can be changed to JSON by setting `-f json`.

```bash
python3 -m itertable example.json         # JSON to CSV
python3 -m itertable -f json example.csv  # CSV to JSON
python3 -m itertable example.xlsx "start_row=5"
python3 -m itertable http://example.com/example.csv
python3 -m itertable itertable.CsvNetIter "url=http://example.com/example.csv"
```

### Extending IterTable

It is straightforward to [extend IterTable][custom] to support arbitrary formats.   Each provided class is composed of a [BaseIter][base] class and mixin classes ([loaders], [parsers], and [mappers]) that handle the various steps of the process.

[wq framework]: https://wq.io/
[csv]: https://docs.python.org/3/library/csv.html
[openpyxl]: https://openpyxl.readthedocs.io/en/stable/
[xml.etree]: https://docs.python.org/3/library/xml.etree.elementtree.html
[iterable]: https://docs.python.org/3/glossary.html#term-iterable
[namedtuples]: https://docs.python.org/3/library/collections.html#collections.namedtuple
[requests]: http://python-requests.org/
[Pandas]: http://pandas.pydata.org/
[DataFrame]: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html
[Fiona]: https://github.com/Toblerity/Fiona
[Shapely]: https://github.com/Toblerity/Shapely

[custom]: https://github.com/wq/itertable/blob/master/docs/about.md
[base]: https://github.com/wq/itertable/blob/master/docs/base.md
[loaders]: https://github.com/wq/itertable/blob/master/docs/loaders.md
[parsers]: https://github.com/wq/itertable/blob/master/docs/parsers.md
[mappers]: https://github.com/wq/itertable/blob/master/docs/mappers.md
[gis]: https://github.com/wq/itertable/blob/master/docs/gis.md
