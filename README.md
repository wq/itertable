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

### [Documentation][docs]

[**Installation**][installation]

[**API**][api]
<br>
[CLI][cli]
&bull;
[GIS][gis]

[**Extending IterTable**][custom]
<br>
[BaseIter][base]
&bull;
[Loaders][loaders]
&bull;
[Parsers][parsers]
&bull;
[Mappers][mappers]

[docs]: https://django-data-wizard.wq.io/itertable/

[installation]: https://django-data-wizard.wq.io/itertable/#getting-started
[api]: https://django-data-wizard.wq.io/itertable/#overview
[cli]: https://django-data-wizard.wq.io/itertable/#command-line-interface
[custom]: https://django-data-wizard.wq.io/itertable/custom
[base]: https://django-data-wizard.wq.io/itertable/base
[loaders]: https://django-data-wizard.wq.io/itertable/loaders
[parsers]: https://django-data-wizard.wq.io/itertable/parsers
[mappers]: https://django-data-wizard.wq.io/itertable/mappers
[gis]: https://django-data-wizard.wq.io/itertable/gis
