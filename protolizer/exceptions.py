class ValidationError(Exception):
    """
    Raised when a validation error occurs.
    Note that this exception is only raised when the serializer is in `is_valid()` mode.
    and raise_exception is passed as `True` on the `is_valid()` call.
    """

    def __init__(self, detail=None):
        self.detail = detail


class InvalidDataError(Exception):

    def __init__(self, field, data=None, expected_type=None, extra=None):
        self.field = field
        self.data = data
        self.expected_type = expected_type
        self.extra = extra

    def __str__(self):
        text = f'Field {self.field} has invalid data: [{self.data}] => [{type(self.data)}]'
        if self.expected_type:
            text += f', expected type: {self.expected_type}'
        if self.extra:
            text += f', extra: {self.extra}'
        return text
