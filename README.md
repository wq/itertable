[![wq.io](https://raw.github.com/wq/wq/master/images/256/wq.io.png)](https://wq.io/wq.io)

[wq.io](https://wq.io/wq.io) is a Pythonic library for consuming (<b>i</b>nput), iterating over, and generating (<b>o</b>utput) external data resources in various formats.  wq.io facilitates <b>i</b>nter<b>o</b>perability between the [wq framework] and other systems and formats. 

wq.io is [designed to be customized], with a [base class] and modular mixin classes that handle [loading], [parsing], and [mapping] external data to a convenient API.


[![Latest PyPI Release](https://img.shields.io/pypi/v/wq.io.svg)](https://pypi.org/project/wq.io)
[![Release Notes](https://img.shields.io/github/release/wq/wq.io.svg)](https://github.com/wq/wq.io/releases)
[![Documentation](https://img.shields.io/badge/Docs-1.1-blue.svg)](https://wq.io/wq.io)
[![License](https://img.shields.io/pypi/l/wq.io.svg)](https://wq.io/license)
[![GitHub Stars](https://img.shields.io/github/stars/wq/wq.io.svg)](https://github.com/wq/wq.io/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/wq/wq.io.svg)](https://github.com/wq/wq.io/network)
[![GitHub Issues](https://img.shields.io/github/issues/wq/wq.io.svg)](https://github.com/wq/wq.io/issues)

[![Travis Build Status](https://img.shields.io/travis/wq/wq.io.svg)](https://travis-ci.org/wq/wq.io)
[![Python Support](https://img.shields.io/pypi/pyversions/wq.io.svg)](https://pypi.python.org/pypi/wq.io)

> Somewhat coincidentally, [https://wq.io](https://wq.io) is also the URL for the website describing the wq framework as a whole.  The documentation for wq.io (the library) is available on wq.io (the website) at <https://wq.io/wq.io>.

## Getting Started

```bash
# Recommended: create virtual environment
# python3 -m venv venv
# . venv/bin/activate

# Install entire wq suite (recommended)
pip install wq

# Install only wq.io
pip install wq.io

# To enable wq.io's GIS support
pip install geopandas # includes Shapely & Fiona

# To enable wq.io's Excel write support
pip install xlwt # xls support
pip install xlsxwriter # xlsx support
# (xls/xlsx read support is enabled by default)
```

See [the wq documentation] for more information.

## Features

wq.io provides a general purpose API for loading, iterating over, and writing tabular datasets.  The basic idea is to avoid needing to remember the unique usage of e.g. [csv], [xlrd], or [xml.etree] every time one needs to work with external data.  Instead, wq.io abstracts these libraries into a consistent interface that works as an [iterable] of [namedtuples].  Whenever possible, the field names for a dataset are automatically determined from the source file, e.g. the column headers in an Excel spreadsheet.

```python
from wq.io import ExcelFileIO
data = ExcelFileIO(filename='example.xls')
for row in data:
    print(row.name, row.date)
```

wq.io provides a number of built-in classes like the above, including a `CsvFileIO`, `XmlFileIO`, and `JsonFileIO`.  There is also a convenience function, `load_file()`, that attempts to automatically determine which class to use for a given file.

```python
from wq.io import load_file
data = load_file('example.csv')
for row in data:
    print(row.name, row.date)
```

All of the included `*FileIO` classes support both reading and writing to external files, though write support for Excel files requires additional libraries ([xlwt] and [xlsxwriter]) that aren't listed as dependencies.

### Network Client

wq.io also provides network-capable equivalents of each of the above classes, to facilitate loading data from third party webservices.

```python
from wq.io import JsonNetIO
class WebServiceIO(JsonNetIO):
    url = "http://example.com/api"
    
data = WebServiceIO(params={'type': 'all'})
for row in data:
    print(row.timestamp, row.value)
```

The powerful [requests] library is used internally to load data over HTTP.

### Pandas Analysis

When [Pandas] is installed, the `as_dataframe()` method on wq.io classes can be used to create a [DataFrame], enabling more extensive analysis possibilities.

```python
instance = WebServiceIO(params={'type': 'all'})
df = instance.as_dataframe()
print(df.value.mean())
```

### GIS Support

When [Fiona] and [Shapely] are installed, wq.io can also open and create shapefiles and other OGR-compatible geographic data formats.

```python
from wq.io import ShapeIO
data = ShapeIO(filename='sites.shp')
for id, site in data.items():
    print(id, site.geometry.wkt)
```

### Extending wq.io
Each `IO` class is composed of mixin classes ([loaders], [parsers], and [mappers]) that handle the various steps of the process.  By extending these mixin or the pre-mixed classes above, it is straightforward to [extend wq.io] to support arbitrary formats.  The [climata library] provides a number of examples of custom `IO` classes for loading climate and hydrology data.


[wq framework]: https://wq.io/
[the wq documentation]: https://wq.io/docs/
[csv]: https://docs.python.org/3/library/csv.html
[xlrd]: http://www.python-excel.org/
[xml.etree]: https://docs.python.org/3/library/xml.etree.elementtree.html
[iterable]: https://docs.python.org/3/glossary.html#term-iterable
[namedtuples]: https://docs.python.org/3/library/collections.html#collections.namedtuple
[requests]: http://python-requests.org/
[xlwt]: http://www.python-excel.org/
[xlsxwriter]: https://xlsxwriter.readthedocs.org/
[Pandas]: http://pandas.pydata.org/
[DataFrame]: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html
[Fiona]: https://github.com/Toblerity/Fiona
[Shapely]: https://github.com/Toblerity/Shapely
[loaders]: https://wq.io/docs/loaders
[parsers]: https://wq.io/docs/parsers
[mappers]: https://wq.io/docs/mappers
[extend wq.io]: https://wq.io/docs/custom-io
[climata library]: https://github.com/heigeo/climata
[designed to be customized]: https://wq.io/docs/custom-io
[base class]: https://wq.io/docs/base-io
[loading]: https://wq.io/docs/loaders
[parsing]: https://wq.io/docs/parsers
[mapping]: https://wq.io/docs/mappers
