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

The basic idea behind wq.io is to avoid having to remember the unique usage of e.g. `csv`, `xlrd`, or `lxml` every time one needs to work with an external dataset.  Instead, wq.io abstracts these libraries into a consistent interface that works as an `iterable` of `namedtuples`.  The field names for a dataset are automatically determined from the source file, e.g. the column headers in an Excel spreadsheet.

```python
from wq.io import load_file
data = load_file('example.xls')
for row in data:
    print row.name, row.date
```

When [fiona] and [shapely] are available, wq.io can also open and create shapefiles and other OGR-compatible geographic data formats.

```python
from wq.io import ShapeIO
data = ShapeIO(filename='sites.shp')
for id, site in data.items():
    print id, site.geometry.wkt
```

It is straightforward to [extend wq.io] by subclassing existing functionality with custom implementations.


[wq.io]: http://wq.io/wq.io
[wq framework]: http://wq.io/
[the documentation]: http://wq.io/docs/
[fiona]: https://github.com/Toblerity/Fiona
[shapely]: https://github.com/Toblerity/Shapely
[extend wq.io]: http://wq.io/docs/custom-io
