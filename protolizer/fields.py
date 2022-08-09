import functools
import inspect
from datetime import datetime
from typing import Any

try:
    from collections import Mapping
except ImportError:
    # Python 3.10 Support
    from collections.abc import Mapping

from protolizer.helpers import DictMapper

__all__ = [
    'Empty',
    'BaseField',
    'BooleanField',
    'CharField',
    'IntField',
    'ObjectIdField',
    'CustomField',
    'set_value'
]


class Empty:
    """
    Empty class to be used as a placeholder for None
    """
    pass


def is_simple_callable(obj):
    """
    True if the object is a callable that takes no arguments.
    """
    # Bail early since we cannot inspect built-in function signatures.
    if inspect.isbuiltin(obj):
        raise ValueError(
            'Built-in function signatures are not injectable. '
            'Wrap the function call in a simple, pure Python function.')

    if not (inspect.isfunction(obj) or inspect.ismethod(obj) or isinstance(obj, functools.partial)):
        return False

    sig = inspect.signature(obj)
    params = sig.parameters.values()
    return all(
        param.kind == param.VAR_POSITIONAL or
        param.kind == param.VAR_KEYWORD or
        param.default != param.empty
        for param in params
    )


def get_attribute(instance, attrs):
    """
    Similar to Python's built in `getattr(instance, attr)`,
    but takes a list of nested attributes, instead of a single attribute.

    Also accepts either attribute lookup on objects or dictionary lookups.
    """
    for attr in attrs:
        try:
            if isinstance(instance, Mapping):
                instance = instance[attr]
            else:
                instance = getattr(instance, attr)
        except (IndexError, KeyError, AttributeError):
            return None
        if is_simple_callable(instance):
            try:
                instance = instance()
            except (AttributeError, KeyError) as exc:
                # If we raised an Attribute or KeyError here it'd get treated
                # as an omitted field in `Field.get_attribute()`. Instead, we
                # raise a ValueError to ensure the exception is not masked.
                raise ValueError(
                    'Exception raised in callable attribute "{}"; original exception was: {}'.format(attr, exc))

    return instance


def set_value(dictionary, keys, value):
    """
    Similar to Python's built in `dictionary[key] = value`,
    but takes a list of nested keys instead of a single key.

    set_value({'a': 1}, [], {'b': 2}) -> {'a': 1, 'b': 2}
    set_value({'a': 1}, ['x'], 2) -> {'a': 1, 'x': 2}
    set_value({'a': 1}, ['x', 'y'], 2) -> {'a': 1, 'x': {'y': 2}}
    """
    if not keys:
        dictionary.update(value)
        return

    for key in keys[:-1]:
        if key not in dictionary:
            dictionary[key] = {}
        dictionary = dictionary[key]

    dictionary[keys[-1]] = value


class BaseField(object):
    _auto_creation_counter = 0
    ALLOWED_TYPES = None
    initial = None

    def __init__(
            self, initial=Empty,
            proto_field: str = None,
            default: Any = None,
            custom: bool = False,
            context: Any = None
    ):
        """
        Initializes the field.
        :param initial: The initial value.
        :param proto_field: proto field is protobuf message field
         it's used when the input data key is different from the output data key.
        :param default: default value for the field.
        :param custom: whether the field is custom. If True, the field will be filled by the custom method.
            custom method name is get_custom_{field_name}.
            note that if the method is not defined, the field will be filled with None.
        :param context: extra context for the field.
        """
        # Increase the auto creation counter
        self._auto_creation_counter = BaseField._auto_creation_counter
        BaseField._auto_creation_counter += 1

        self.initial = self.initial if (initial is Empty) else initial
        self.proto_field = proto_field
        self.default = default
        self.custom = custom
        self.context = {} if context is None else context

        # These are set up by `.bind()` when the field is added to a serializer.
        self.field_name = None
        self.parent = None
        self.source = None
        self.attributes = None

        self.meta = getattr(self, 'Meta', None)
        self.pb = getattr(self.meta, 'schema', None) if self.meta else None

    def bind(self, field_name, parent):
        """
        Initializes the field name and parent for the field instance.

        :param field_name: The field name.
        :param parent: The parent field.
        :return: None
        """
        self.field_name = field_name
        self.parent = parent

        # self.source should default to being the same as the field name.
        if self.source is None:
            self.source = field_name

        if self.source == '*':
            self.attributes = []
        else:
            self.attributes = self.source.split('.')

    def get_initial(self):
        return self.initial() if callable(self.initial) else self.initial

    def get_value(self, dictionary, instance):
        """
        Given the *incoming* dictionary, return the value for this field
        that should be validated and transformed to a native value.
        """

        # convert the dictionary to mapping to make it easier to work with
        dictionary = DictMapper(dictionary) if isinstance(dictionary, dict) else dictionary

        if self.custom:
            fill_method = getattr(instance, f'get_custom_{self.field_name}', None)
            return fill_method(dictionary) if fill_method else None

        return dictionary[self.field_name] if self.field_name in dictionary and not self.custom else Empty

    def get_attribute(self, instance):
        """
        Given the *outgoing* instance, return the value for this field
        that should be serialized.
        """
        return get_attribute(instance, self.attributes)

    def get_default(self):
        """
        Return the default value for this field.
        """
        return self.default

    def validate_empty_values(self, data):
        """
        Validate empty values, and either:
        """
        if data is Empty:
            return True, self.get_default()

        if data is None:
            if self.source == '*':
                return False, None
            return True, None

        return False, data

    def run_validation(self, data=Empty):
        """
        Run default validation on fields.
        """
        (is_empty_value, data) = self.validate_empty_values(data)
        if is_empty_value:
            return data

        return self.to_internal_value(data)

    def to_internal_value(self, data):
        """
        Given the *incoming* primitive data, return the native value.
        """
        raise NotImplementedError('`to_internal_value()` must be implemented.')

    def to_representation(self, value):
        """
        Given the native value, return the representation of this field
        that should be returned to the user.
        """
        raise NotImplementedError('`to_representation()` must be implemented.')

    def to_protobuf(self, data):
        """
        Given the native value, return the protobuf value.
        """
        raise NotImplementedError('`to_protobuf()` must be implemented.')

    @property
    def root(self):
        """
        Returns the top-level serializer for this field.
        """
        root = self
        while root.parent is not None:
            root = root.parent
        return root

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._args = args
        instance._kwargs = kwargs
        return instance


class BooleanField(BaseField):
    TRUE_VALUES = ['t', 'T', 'true', 'True', 'TRUE', '1', 1, True]
    FALSE_VALUES = ['f', 'F', 'false', 'False', 'FALSE', '0', 0, False]
    NULL_VALUES = ['n', 'N', 'null', 'Null', 'NULL', '', None]

    def to_internal_value(self, data):
        if data is not Empty:
            if data in self.TRUE_VALUES:
                return True
            elif data in self.FALSE_VALUES:
                return False
            elif data in self.NULL_VALUES:
                return None
            raise ValueError('Invalid boolean value.')
        return data

    def to_representation(self, value):
        if value in self.TRUE_VALUES:
            return True
        elif value in self.FALSE_VALUES:
            return False
        elif value in self.NULL_VALUES:
            return None
        return bool(value)

    def to_protobuf(self, value):
        _repr = self.to_representation(value)
        if _repr is None:
            return None
        return _repr


class CharField(BaseField):
    """
    A field that validates input as a string.
    """
    def __init__(self, **kwargs):
        self.trim_whitespace = kwargs.pop('trim_whitespace', True)
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        value = str(data)
        return value.strip() if self.trim_whitespace else value

    def to_representation(self, value):
        return str(value) if value is not None else None

    def to_protobuf(self, value):
        _repr = self.to_representation(value)
        if _repr is None:
            return None
        return _repr


class IntField(BaseField):
    """
    A field that validates input as an integer.
    """

    def to_internal_value(self, data):
        try:
            return int(data)
        except (TypeError, ValueError):
            raise ValueError('Expected a number.')

    def to_representation(self, value):
        return int(value) if value is not None else None

    def to_protobuf(self, value):
        _repr = self.to_representation(value)
        if _repr is None:
            return None
        return _repr


class FloatField(BaseField):
    """
    A field that validates input as a float.
    """

    def to_internal_value(self, data):
        try:
            return float(data)
        except (TypeError, ValueError):
            raise ValueError('Expected a number.')

    def to_representation(self, value):
        return float(value) if value is not None else None

    def to_protobuf(self, value):
        _repr = self.to_representation(value)
        if _repr is None:
            return None
        return _repr


class ObjectIdField(BaseField):
    """
    A field that validates input as an ObjectId.
    """

    def to_internal_value(self, data):
        return str(data)

    def to_representation(self, value):
        return str(value)

    def to_protobuf(self, value):
        _repr = self.to_representation(value)
        if _repr is None:
            return None
        return _repr


class CustomField(BaseField):
    """
    A field that validates input as a custom field.
    custom fields are defined in the model class
    e.g:
        class MyModel(Model):
            username = CustomField()

            def get_custom_username(obj):
                return "John Doe"
    """
    def __init__(self, child=None):
        self.child = child
        super().__init__(custom=True)

    def to_internal_value(self, data):
        if data is not Empty:
            if not self.child:
                return data

            if isinstance(data, list):
                return [self.child.to_internal_value(item) for item in data]
            return self.child.to_internal_value(data)
        return data

    def to_representation(self, value):
        if not self.child:
            return value
        if isinstance(value, list):
            [self.child.to_representation(item) for item in value]
        return self.child.to_representation(value)

    def to_protobuf(self, value):
        _repr = self.to_representation(value)
        if _repr is None:
            return None
        return _repr


class ListField(BaseField):
    """
    A field that validates input as a list.
    """

    ALLOWED_TYPES = [
        'CharField', 'DateTimeField', 'IntField',
        'ObjectIdField', 'CustomField', 'BooleanField',
        'FloatField'
    ]

    def __init__(self, child=None, **kwargs):
        self.type = child
        if child and child.__class__.__name__ not in self.ALLOWED_TYPES:
            raise ValueError(
                'type {!r} is not allowed for {!r}. '
                'Allowed types are: {}'.format(
                    child.__class__.__name__,
                    self.__class__.__name__,
                    ', '.join(self.ALLOWED_TYPES)
                )
            )
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if data is not Empty:
            if not self.type:
                return data
            return [self.type.to_internal_value(item) for item in data]
        return data

    def to_representation(self, value):
        if not self.type:
            return value
        return [self.type.to_representation(item) for item in value]

    def to_protobuf(self, value):
        _repr = self.to_representation(value)
        if _repr is None:
            return None
        return _repr


class DictField(BaseField):
    """
    A field that validates input as a dict.
    """

    ALLOWED_TYPES = ['ListField']

    def __init__(self, child=None, **kwargs):
        self.type = child
        if child and child.__class__.__name__ not in self.ALLOWED_TYPES:
            raise ValueError(
                'type {!r} is not allowed for {!r}. '
                'Allowed types are: {}'.format(
                    child.__class__.__name__,
                    self.__class__.__name__,
                    ', '.join(self.ALLOWED_TYPES)
                )
            )

        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if data is not Empty:
            if not self.type:
                return data
            return {
                key: self.type.to_internal_value(value)
                for key, value in data.items()
            }
        return data

    def to_representation(self, value):
        if not self.type:
            return value
        return {
            key: self.type.to_representation(item)
            for key, item in value.items()
        }

    def to_protobuf(self, value):
        _repr = self.to_representation(value)
        if _repr is None:
            return None
        return _repr


class DateTimeField(BaseField):
    """
    A field that validates input as a datetime.
    """

    def __init__(self, fmt='%Y-%m-%dT%H:%M:%S', **kwargs):
        self.format = fmt
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if data is not Empty:
            if isinstance(data, datetime):
                return data.strftime(self.format) if self.format else data
            if self.format:
                data = datetime.strptime(data, self.format)
            else:
                data = datetime.fromtimestamp(data)
            return data
        return data

    def to_representation(self, value):
        if value is not None:
            if self.format and isinstance(value, datetime):
                return value.strftime(self.format)
            return value
        return value

    def to_protobuf(self, value):
        _repr = self.to_representation(value)
        if _repr is None:
            return None
        return _repr


class TimestampField(BaseField):
    """
    A field that validates input as a timestamp.
    """

    ALLOWED_TYPES = ['IntField', 'CharField', 'FloatField']

    def __init__(self, child=None, **kwargs):
        self.type = IntField() if child is None else child
        if child and child.__class__.__name__ not in self.ALLOWED_TYPES:
            raise ValueError(
                'type {!r} is not allowed for {!r}. '
                'Allowed types are: {}'.format(
                    child.__class__.__name__,
                    self.__class__.__name__,
                    ', '.join(self.ALLOWED_TYPES)
                )
            )
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if data is not Empty:
            if isinstance(data, datetime):
                return data.timestamp()
            return self.type.to_internal_value(data)
        return data

    def to_representation(self, value):
        if value is not None:
            if isinstance(value, datetime):
                return value.timestamp()
            return self.type.to_representation(value)
        return value

    def to_protobuf(self, value):
        _repr = self.to_representation(value)
        if _repr is None:
            return None
        return _repr
