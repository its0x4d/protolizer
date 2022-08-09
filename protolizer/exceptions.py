class ValidationError(Exception):
    """
    Raised when a validation error occurs.
    Note that this exception is only raised when the serializer is in `is_valid()` mode.
    and raise_exception is passed as `True` on the `is_valid()` call.
    """
    def __init__(self, detail=None):
        self.detail = detail
