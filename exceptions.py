class IoException(Exception):
    pass


class LoadFailed(IoException):
    def __init__(self, message, content=None, path=None, code=None):
        super(LoadFailed, self).__init__(message)
        self.content = content
        self.path = path
        self.code = code

    def __str__(self):
        if self.content is not None:
            return self.content
        elif self.code is not None:
            return "%s Error" % self.code
        return super(LoadFailed, self).__str__()


class ParseFailed(IoException):
    pass


class MappingFailed(IoException):
    pass


class NoData(IoException):
    pass
