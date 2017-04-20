from collections import namedtuple, OrderedDict
import re
from datetime import datetime
from wq.io.exceptions import NoData, MappingFailed
from unicodedata import normalize


class BaseMapper(object):
    def get_key_field(self):
        return self.map_field(self.key_field)

    def map_field(self, field):
        return field

    def map_value(self, field, value):
        return value

    def unmap_field(self, field):
        return field

    def unmap_value(self, field, value):
        return value

    def usable_item(self, item):
        uitem = {}
        for key, val in item.items():
            field = self.map_field(key)
            value = self.map_value(field, val)
            uitem[field] = value
        return uitem

    def parse_usable_item(self, uitem):
        item = {}
        for field, value in uitem.items():
            key = self.unmap_field(field)
            val = self.unmap_value(field, value)
            item[key] = val
        return item


class DictMapper(BaseMapper):
    field_map = {}
    value_map = {}

    def map_field(self, field):
        field = self.field_map[field] if field in self.field_map else field
        return field

    def map_value(self, field, value):
        if not isinstance(value, str):
            return value
        value = self.value_map[value] if value in self.value_map else value
        return value

    def unmap_field(self, field):
        for f in self.field_map:
            if self.field_map[f] == field:
                return f
        return field

    def unmap_value(self, field, value):
        if not isinstance(value, str):
            return value
        for v in self.value_map:
            if self.value_map[v] == value:
                return v
        return value


class TupleMapper(DictMapper):
    no_pickle_mapper = ['_tuple_class', '_tuple_prototype']

    @property
    def field_map(self):
        field_names = self.get_field_names()
        if not field_names and not getattr(self, 'data', None):
            raise NoData

        # FIXME: check for duplicates
        if not hasattr(self, '_field_map'):
            items = [
                (field, self.tuple_field_name(field))
                for field in field_names
            ]
            self._field_map = OrderedDict(items)
        return self._field_map

    def tuple_field_name(self, field):
        field = self.clean_field_name(field)
        field = re.sub(r'\W', '', field.lower())
        try:
            # normalize identifiers for consistency with namedtuple
            # http://bugs.python.org/issue23091
            field = normalize('NFKC', field)
        except TypeError:
            # normalize doesn't work on Python 2 str() instances
            pass
        return field

    def clean_field_name(self, field):
        return field

    @property
    def tuple_class(self):
        "Returns a class to use for individual items"

        if not hasattr(self, '_tuple_class'):
            cls = namedtuple(
                self.__class__.__name__ + 'Tuple',
                list(self.field_map.values())
            )
            self._tuple_class = cls

        return self._tuple_class

    @property
    def tuple_prototype(self):
        if not hasattr(self, '_tuple_prototype'):
            vals = {field: None for field in self.field_map.values()}
            self._tuple_prototype = self.tuple_class(**vals)
        return self._tuple_prototype

    def usable_item(self, item):
        mapped = super(TupleMapper, self).usable_item(item)
        try:
            return self.tuple_prototype._replace(**mapped)
        except ValueError as e:
            raise MappingFailed(str(e))

    def parse_usable_item(self, uitem):
        mapped = {key: getattr(uitem, key) for key in self.field_map.values()}
        return super(TupleMapper, self).parse_usable_item(mapped)

    def item_dict(self, uitem):
        return uitem._asdict()

    def create(self, **kwargs):
        return self.tuple_prototype._replace(**kwargs)


def parse_iso8601(val):
    # See http://bugs.python.org/issue15873
    if hasattr(datetime, 'fromisoformat'):
        return datetime.fromisoformat(val)
    try:
        from django.utils.dateparse import parse_datetime
    except ImportError:
        try:
            from iso8601 import parse_date as parse_datetime
        except ImportError:
            raise Exception('No suitable iso8601 parser found!')
    result = parse_datetime(val)
    if result is None:
        raise ValueError("Could not parse %s as iso8601 date!" % val)
    return result


def make_date_mapper(fmt):
    """
    Generate functions to use for mapping strings to dates
    """
    def mapper(val):
        if fmt == 'iso8601':
            return parse_iso8601(val)
        val = datetime.strptime(val, fmt)
        if '%Y' in fmt or '%y' in fmt:
            return val
        else:
            return val.time()
    return mapper


class TimeSeriesMapper(TupleMapper):
    date_formats = None
    map_floats = True
    map_functions = []

    def make_date_mapper(self, fmt):
        return make_date_mapper(fmt)

    def map_value(self, field, value):
        if not isinstance(value, str):
            return value

        if not self.map_functions:
            self.map_functions = [
                self.make_date_mapper(fmt) for fmt in self.date_formats
            ]

            if self.map_floats:
                self.map_functions.insert(0, float)

        value = value.strip()
        for i, fn in enumerate(self.map_functions):
            try:
                return fn(value)
            except ValueError:
                pass
        return value

    @property
    def key_fields(self):
        raise NotImplementedError("Key fields must be specified")

    def parameter_fields(self):
        return sorted(set(self.field_map.values()) - set(self.key_fields))
