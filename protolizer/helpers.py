from collections import OrderedDict
try:
    from collections import Mapping, MutableMapping
except ImportError:
    # Python 3.10 support
    from collections.abc import Mapping, MutableMapping


class BoundField:
    """
    A field object that also includes `.value` and `.error` properties.
    Returned when iterating over a serializer instance,
    providing an API similar to Django forms and form fields.
    """

    def __init__(self, field, value, errors, prefix=''):
        self._field = field
        self._prefix = prefix
        self.value = value
        self.errors = errors
        self.name = prefix + self.field_name

    def __getattr__(self, attr_name):
        return getattr(self._field, attr_name)

    @property
    def _proxy_class(self):
        return self._field.__class__

    def __repr__(self):
        return '<%s value=%s errors=%s>' % (
            self.__class__.__name__, self.value, self.errors
        )


class NestedBoundField(BoundField):
    """
    This `BoundField` additionally implements __iter__ and __getitem__
    in order to support nested bound fields. This class is the type of
    `BoundField` that is used for serializer fields.
    """

    def __init__(self, field, value, errors, prefix=''):
        if value is None or value == '' or not isinstance(value, Mapping):
            value = {}
        super().__init__(field, value, errors, prefix)

    def __iter__(self):
        for field in self.fields.values():
            yield self[field.field_name]

    def __getitem__(self, key):
        field = self.fields[key]
        value = self.value.get(key) if self.value else None
        error = self.errors.get(key) if isinstance(self.errors, dict) else None
        if hasattr(field, 'fields'):
            return NestedBoundField(field, value, error, prefix=self.name + '.')
        return BoundField(field, value, error, prefix=self.name + '.')


class BindingDict(MutableMapping):
    """
    This dict-like object is used to store fields on a serializer.
    This ensures that whenever fields are added to the serializer we call
    `field.bind()` so that the `field_name` and `parent` attributes
    can be set correctly.
    """

    def __init__(self, serializer):
        self.serializer = serializer
        self.fields = OrderedDict()

    def __setitem__(self, key, field):
        self.fields[key] = field
        field.bind(field_name=key, parent=self.serializer)

    def __getitem__(self, key):
        return self.fields[key]

    def __delitem__(self, key):
        del self.fields[key]

    def __iter__(self):
        return iter(self.fields)

    def __len__(self):
        return len(self.fields)

    def __repr__(self):
        return dict.__repr__(self.fields)


class ReturnList(list):
    """
    Return object from `serializer.data` for the `SerializerList` class.
    Includes a backlink to the serializer instance for renderers
    to use if they need richer field information.
    """

    def __init__(self, *args, **kwargs):
        self.serializer = kwargs.pop('serializer')
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return list.__repr__(self)

    def __reduce__(self):
        # Pickling these objects will drop the .serializer backlink,
        # but preserve the raw data.
        return list, (list(self),)


class ReturnDict(OrderedDict):
    """
    Return object from `serializer.data` for the `Serializer` class.
    Includes a backlink to the serializer instance for renderers
    to use if they need richer field information.
    """

    def __init__(self, *args, **kwargs):
        self.serializer = kwargs.pop('serializer')
        super().__init__(*args, **kwargs)

    def copy(self):
        return ReturnDict(self, serializer=self.serializer)

    def __repr__(self):
        return dict.__repr__(self)

    def __reduce__(self):
        # Pickling these objects will drop the .serializer backlink,
        # but preserve the raw data.
        return dict, (dict(self),)


class DictMapper(dict):
    """
    This is a dict-like object that exposes keys as attributes.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self:
            self.__dict__[key] = self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        del self[key]

    def __getattr__(self, key):
        return self[key]

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.__dict__[key] = value

    def __delitem__(self, key):
        super().__delitem__(key)
        del self.__dict__[key]

    def __repr__(self):
        return dict.__repr__(self)
