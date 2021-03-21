class ValidationError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class RentingError(ValidationError):
    def __init__(self, message):
        Exception.__init__(self, message)


class RepositoryError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class InputError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class DateError(InputError):
    def __init__(self, message):
        Exception.__init__(self, message)


class TimelineError(InputError):
    def __init__(self, message):
        Exception.__init__(self, message)

class UndoError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)