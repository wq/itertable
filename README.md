# wq.io

Python libraries for consuming (input) and generating (output) external data
resources in various formats.

## Importing data

The basic process is broken into several steps which are handed by various
submodules.

**loaders**

  Load an external resource from the local filesystem or from the web
  into a file-like object.

**parsers**

  Parse the file (using the standard python library for that file type) and
  convert the recordset into a simple list of dictionaries.

**mappers**

  Rename field names and values if needed and optionally convert the
  dictionaries into other object types (such as a namedtuple).

## Traversing data

The base library then provides a collection object (an "IO") that can be used
to easily navigate the dataset.  It also provides a number of convenience
classes for common IO use cases.  For example, CsvNetIO provides an IO with
loaders.NetLoader, parsers.CsvParser, and mappers.TupleMapper pre-mixed into
the class.

## Exporting data 

The export process uses the same submodules to apply the above steps in
reverse:

**mappers**

  Convert the mapped object back into a simple dictionary and map the field
  names and values back to the format expected by the file.

**parsers**

  Convert the dictionary list back into the source format and write out to the
  file.

**loaders**

  Prepare the file-like object for writing and perform any needed wrap-up
  operations.
