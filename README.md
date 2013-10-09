[![wq.io](https://raw.github.com/wq/wq/master/images/256/wq.io.png)](http://wq.io/wq.io)

**[wq.io](http://wq.io/wq.io)** is a collection of Python libraries for consuming (<b>i</b>nput) and generating (<b>o</b>utput) external data resources in various formats.  It thereby facilitates <b>i</b>nter<b>o</b>perability between the [wq framework](http://wq.io) and other systems and formats.

The basic idea behind wq.io is to avoid having to remember the unique usage of e.g. `csv`, `xlrd`, or `lxml` every time one needs to work with an external dataset.  Instead, wq.io abstracts these libraries into a consistent interface that works as an `iterable` of `namedtuples`.

### Example

```python
from wq.io import load_file
data = load_file('example.xls')
for row in data:
    print row.name, row.date
```

## Extending wq.io

The actual process is broken into several steps (`load`, `parse`, and `map`) which are handed by various mixins.  These are mixed with the `BaseIO` class to provide a usable class that can load and iterate over files.

### Example

```python
from wq.io import make_io
from wq.io.loaders import FileLoader
from wq.io.parsers import JsonParser

class MyJsonParser(JsonParser):
    def parse(self):
    # custom parsing code ...
    
MyJsonFileIO = make_io(FileLoader, MyJsonParser)

for record in MyJsonFileIO(filename='file.json'):
    print record.id
```

### `loaders`

Load an external resource from the local filesystem or from the web into a file-like object.  On export, loaders prepare the file-like object for writing and perform any needed wrap-up operations.

### `parsers`

Parse the file (usually using the standard python library for that file type) and convert the recordset into a simple list of dictionaries.  On export, parsers coonvert the dictionary list back into the source format and write out to the file.

### `mappers`

Rename field names and values if needed and optionally convert the dictionaries into other object types (such as a namedtuple).  On export, mappers convert the mapped object back into a simple dictionary and map the field names and values back to the format expected by the file.

