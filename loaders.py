from httplib2 import Http
from StringIO import StringIO
from urllib import urlencode


class BaseLoader(object):
    def load(self):
        raise NotImplementedError


class FileLoader(BaseLoader):
    filename = None

    def load(self):
        try:
            self.file = open(self.filename)
        except:
            self.file = StringIO()

    def save(self):
        file = open(self.filename, 'w+')
        self.dump(file)
        file.close()
        self.load()


class BinaryFileLoader(FileLoader):
    def load(self):
        self.file = open(self.filename, 'rb')


class StringLoader(BaseLoader):
    string = ""

    def load(self):
        self.file = StringIO(self.string)

    def save(self):
        file = StringIO()
        self.dump(file)
        self.string = file.getvalue()
        file.close()
        self.load()


class NetLoader(BaseLoader):
    "NetLoader: opens HTTP/REST resources for use in wq.io"

    username = None
    password = None
    headers = {}

    http = Http()

    @property
    def url(self):
        raise NotImplementedError

    def load(self, **kwargs):

        if self.username is not None and self.password is not None:
            self.http.add_credentials(self.username, self.password)

        content = self.GET()
        self.file = StringIO(content)

    def req(self, url=None, method=None, params=None, body=None, headers={}):
        if url is None:
            url = self.url

        if params is None:
            params = getattr(self, 'params', None)

        if params is not None:
            url += '?' + urlencode(params)

        all_headers = self.headers.copy()
        all_headers.update(headers)

        resp, content = self.http.request(
            url, method=method, body=body, headers=all_headers
        )
        if resp.status < 200 or resp.status > 299:
            raise Exception(url + '\n' + content)

        return content

    def GET(self, **kwargs):
        return self.req(method='GET', **kwargs)

    def POST(self, **kwargs):
        return self.req(method='POST', **kwargs)

    def PUT(self, **kwargs):
        return self.req(method='PUT', **kwargs)

    def DELETE(self, **kwargs):
        return self.req(method='DELETE', **kwargs)
