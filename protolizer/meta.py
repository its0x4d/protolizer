from collections import OrderedDict

from protolizer.fields import BaseField


class SerializerMetaclass(type):
    """
    This metaclass sets a dictionary named `_declared_fields` on the class.
    Any instances of `Field` included as attributes on either the class
    or on any of its superclasses will be included in the
    `_declared_fields` dictionary.
    """

    @classmethod
    def _get_declared_fields(mcs, bases, attrs):
        fields = [(field_name, attrs.pop(field_name))
                  for field_name, obj in list(attrs.items())
                  if isinstance(obj, BaseField)]
        fields.sort(key=lambda x: x[1]._auto_creation_counter)  # noqa

        # Ensures a base class field doesn't override cls attrs, and maintains
        # field precedence when inheriting multiple parents. e.g. if there is a
        # class C(A, B), and A and B both define 'field', use 'field' from A.
        known = set(attrs)

        def visit(name):
            known.add(name)
            return name

        base_fields = [
            (visit(name), f)
            for base in bases if hasattr(base, '_declared_fields')
            for name, f in base._declared_fields.items() if name not in known # noqa
        ]

        return OrderedDict(base_fields + fields)

    def __new__(mcs, name, bases, attrs):
        attrs['_declared_fields'] = mcs._get_declared_fields(bases, attrs)
        return super().__new__(mcs, name, bases, attrs)
