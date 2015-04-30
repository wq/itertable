from __future__ import print_function
import requests
try:
    # Python 2 (uses str)
    from StringIO import StringIO
except ImportError:
    # Python 3 (Python 2 equivalent uses unicode)
    from io import StringIO
from io import BytesIO
from wq.io.version import VERSION
from .exceptions import LoadFailed
from zipfile import ZipFile


class BaseLoader(object):
    no_pickle_loader = ['file']
    empty_file = None
    binary = False

    def load(self):
        raise NotImplementedError


class FileLoader(BaseLoader):
    filename = None
    read_mode = 'r'
    write_mode = 'w+'

    def load(self):
        try:
            self.file = open(self.filename, self.read_mode)
            self.empty_file = False
        except IOError:
            if self.binary:
                self.file = BytesIO()
            else:
                self.file = StringIO()
            self.empty_file = True

    def save(self):
        file = open(self.filename, self.write_mode)
        self.dump(file)
        file.close()


class BinaryFileLoader(FileLoader):
    binary = True
    read_mode = 'rb'
    write_mode = 'wb+'


class Zipper(object):
    inner_filename = None
    inner_binary = False

    def unzip_file(self):
        zipfile = ZipFile(self.file)
        inner_file = zipfile.read(
            self.get_inner_filename(zipfile)
        )
        if self.inner_binary:
            self.file = BytesIO(inner_file)
        else:
            self.file = StringIO(inner_file.decode('utf-8'))
        zipfile.fp.close()
        zipfile.close()

    def get_inner_filename(self, zipfile):
        if self.inner_filename:
            return self.inner_filename
        names = zipfile.namelist()
        if len(names) == 1:
            return names[0]

        zipfile.fp.close()
        zipfile.close()
        raise LoadFailed("Multiple Inner Files!")


class ZipFileLoader(Zipper, BinaryFileLoader):
    def load(self):
        super(ZipFileLoader, self).load()
        self.unzip_file()


class StringLoader(BaseLoader):
    string = ""

    def load(self):
        self.file = StringIO(self.string)

    def save(self):
        file = StringIO()
        self.dump(file)
        self.string = file.getvalue()
        file.close()


class NetLoader(BaseLoader):
    "NetLoader: opens HTTP/REST resources for use in wq.io"

    username = None
    password = None
    debug = False
    url = None

    @property
    def user_agent(self):
        return "wq.io/%s (%s)" % (VERSION, requests.utils.default_user_agent())

    @property
    def headers(self):
        return {
            'User-Agent': self.user_agent,
        }

    def load(self, **kwargs):
        result = self.GET()
        if self.binary:
            self.file = BytesIO(result)
        else:
            self.file = StringIO(result)

    def req(self, url=None, method=None, params=None, body=None, headers={}):
        if url is None:
            url = self.url
            if url is None:
                raise LoadFailed("No URL provided")

        if params is None:
            params = getattr(self, 'params', None)

        if isinstance(params, str):
            url += '?' + params
            params = None

        if self.debug:
            if params:
                from requests.compat import urlencode
                debug_url = url + '?' + urlencode(params, doseq=True)
            else:
                debug_url = url
            self.debug_string = "%s: %s" % (method, debug_url)
            print(self.debug_string)

        if self.username is not None and self.password is not None:
            auth = (self.username, self.password)
        else:
            auth = None

        all_headers = self.headers.copy()
        all_headers.update(headers)

        resp = requests.request(
            method, url,
            params=params,
            headers=all_headers,
            auth=auth,
            data=body,
        )

        if resp.status_code < 200 or resp.status_code > 299:
            raise LoadFailed(
                resp.text,
                path=url,
                code=resp.status_code,
            )

        if self.binary:
            return resp.content
        else:
            return resp.text

    def GET(self, **kwargs):
        return self.req(method='GET', **kwargs)

    def POST(self, **kwargs):
        return self.req(method='POST', **kwargs)

    def PUT(self, **kwargs):
        return self.req(method='PUT', **kwargs)

    def DELETE(self, **kwargs):
        return self.req(method='DELETE', **kwargs)


class ZipNetLoader(Zipper, NetLoader):
    binary = True

    def load(self):
        super(ZipNetLoader, self).load()
        self.unzip_file()
