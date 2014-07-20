[![wq.io](https://raw.github.com/wq/wq/master/images/256/wq.io.png)](http://wq.io/wq.io)

[wq.io] is a collection of Python libraries for consuming (<b>i</b>nput) and generating (<b>o</b>utput) external data resources in various formats.  It thereby facilitates <b>i</b>nter<b>o</b>perability between the [wq framework] and other systems and formats.

[![Build Status](https://travis-ci.org/wq/wq.io.png?branch=master)](https://travis-ci.org/wq/wq.io)

## Getting Started

```bash
pip install wq.io
# Or, if using together with wq.app and/or wq.db
pip install wq
# To use wq.io's GIS capabilities also install Shapely and Fiona
pip install shapely fiona
```

See [the documentation] for more information.

## Features

wq.io provides a general purpose API for loading, iterating over, and writing tabular datasets.  The basic idea is to avoid needing to remember the unique usage of e.g. [csv], [xlrd], or [xml.etree] every time one needs to work with an external dataset.  Instead, wq.io abstracts these libraries into a consistent interface that works as an `iterable` of `namedtuples`.  Whenever possible, the field names for a dataset are automatically determined from the source file, e.g. the column headers in an Excel spreadsheet.

```python
from wq.io import ExcelFileIO
data = ExcelFileIO(filename='example.xls')
for row in data:
    print row.name, row.date
```

wq.io provides a number of builtin classes like the above, including a `CsvFileIO`, `XmlFileIO`, and `JsonFileIO`.  There is also a convenience function, `load_file`, that automatically determines which class to use for a given file.

```python
from wq.io import load_file
data = load_file('example.csv')
for row in data:
    print row.name, row.date
```

All of the `*FileIO` classes support both reading and writing to external files.

### Network Client

wq.io also provides network-capable equivalents of each of the above classes, to facilitate loading data from third party webservices.

```python
from wq.io import JsonNetIO
class WebServiceIO(JsonNetIO):
    url = "http://example.com/api"
    
data = WebServiceIO(params={'type': 'all'})
for row in data:
    print row.timestamp, row.value
```

The powerful [requests] library is used internally to load data over HTTP.

### GIS Support

When [fiona] and [shapely] are available, wq.io can also open and create shapefiles and other OGR-compatible geographic data formats.

```python
from wq.io import ShapeIO
data = ShapeIO(filename='sites.shp')
for id, site in data.items():
    print id, site.geometry.wkt
```

### Extending wq.io
Each `IO` class is composed of mixin classes ([loaders], [parsers], and [mappers]) that handle the various steps of the process.  By extending these mixin or the pre-mixed classes above, it is straightforward to [extend wq.io] to support arbitrary formats.


[wq.io]: http://wq.io/wq.io
[wq framework]: http://wq.io/
[the documentation]: http://wq.io/docs/
[csv]: https://docs.python.org/3/library/csv.html
[xlrd]: http://www.python-excel.org/
[xml.etree]: https://docs.python.org/3/library/xml.etree.elementtree.html
[requests]: http://python-requests.org/
[fiona]: https://github.com/Toblerity/Fiona
[shapely]: https://github.com/Toblerity/Shapely
[loaders]: http://wq.io/docs/loaders
[parsers]: http://wq.io/docs/parsers
[mappers]: http://wq.io/docs/mappers
[extend wq.io]: http://wq.io/docs/custom-io
