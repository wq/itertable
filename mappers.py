from collections import namedtuple, OrderedDict
import re


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
        for key, val in item.iteritems():
            field = self.map_field(key)
            value = self.map_value(field, val)
            uitem[field] = value
        return uitem

    def parse_usable_item(self, uitem):
        item = {}
        for field, value in uitem.iteritems():
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
        if not isinstance(value, basestring):
            return value
        value = self.value_map[value] if value in self.value_map else value
        return value

    def unmap_field(self, field):
        for f in self.field_map:
            if self.field_map[f] == field:
                return f
        return field

    def unmap_value(self, field, value):
        if not isinstance(value, basestring):
            return value
        for v in self.value_map:
            if self.value_map[v] == value:
                return v
        return value


class TupleMapper(DictMapper):
    @property
    def field_map(self):
        #FIXME: check for duplicates
        if not hasattr(self, '_field_map'):
            field_names = self.get_field_names()
            items = [
                (field, re.sub(r'\W', '', field.lower()))
                for field in field_names
            ]
            self._field_map = OrderedDict(items)
        return self._field_map

    @property
    def tuple_class(self):
        "Returns a class to use for individual items"

        if not hasattr(self, '_item_class'):
            cls = namedtuple(
                self.__class__.__name__ + 'Tuple',
                self.field_map.values()
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
        return self.tuple_prototype._replace(**mapped)

    def parse_usable_item(self, uitem):
        mapped = {key: getattr(uitem, key) for key in self.field_map.values()}
        return super(TupleMapper, self).parse_usable_item(mapped)

    def create(self, **kwargs):
        return self.tuple_prototype._replace(**kwargs)
