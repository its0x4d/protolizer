class ValidationError(Exception):

    def __init__(self, detail=None):
        self.detail = detail
