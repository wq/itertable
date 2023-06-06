try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None


class IterException(Exception):
    def __str__(self):
        if self.args and self.args[0]:
            return self.args[0]
        return self.__doc__


class LoadFailed(IterException):
    """Error loading data!"""

    def __init__(self, message, path=None, code=None):
        super(LoadFailed, self).__init__(message)
        self.path = path
        self.code = code

    def __str__(self):
        if self.args and self.args[0]:
            text = self.args[0]
            has_html = False
            for tag in "<html", "<body", "<div":
                if tag in text or tag.upper() in text:
                    has_html = True
            if has_html and BeautifulSoup:
                html = BeautifulSoup(text).body
                if html:
                    text = html.get_text("\n")
            return text
        elif self.code is not None:
            return "%s Error" % self.code
        return super(LoadFailed, self).__str__()


class ParseFailed(IterException):
    """Error parsing data!"""

    pass


class MappingFailed(IterException):
    """Error processing data!"""

    pass


class NoData(IterException):
    """No data returned!"""

    pass
