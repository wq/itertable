import unittest
import httpretty
from wq.io import CsvNetIO
from wq.io.exceptions import LoadFailed
import pickle
from .base import IoTestCase


class TestIO(CsvNetIO):
    url = "http://example.com/test.csv"


class NetLoaderTestCase(IoTestCase):
    def setUp(self):
        httpretty.enable()

        httpretty.register_uri(
            httpretty.GET,
            "http://example.com/test.csv",
            body="one,two,three\n1,2,3\n4,5,6",
            content_type="text/csv"
        )
        httpretty.register_uri(
            httpretty.GET,
            "http://example.com/fail.txt",
            body="Not Found",
            content_type="text/plain",
            status=404,
        )
        httpretty.register_uri(
            httpretty.GET,
            "http://example.com/fail.html",
            body="<html><body>Not Found</body></html>",
            content_type="text/html",
            status=404,
        )

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def test_load_csv(self):
        self.check_instance(TestIO())

    def test_load_csv_params(self):
        self.check_instance(TestIO(params={'test': 1}))
        qs = httpretty.last_request().querystring
        self.assertEqual(qs, {'test': ['1']})

        self.check_instance(TestIO(params="test=1"))
        qs = httpretty.last_request().querystring
        self.assertEqual(qs, {'test': ['1']})

        self.check_instance(TestIO(params=None))
        qs = httpretty.last_request().querystring
        self.assertEqual(qs, {})

    def test_debug_string(self):
        instance = TestIO(debug=True)
        self.assertEqual(
            instance.debug_string, "GET: http://example.com/test.csv"
        )
        instance = TestIO(params={'test': 1}, debug=True)
        self.assertEqual(
            instance.debug_string, "GET: http://example.com/test.csv?test=1"
        )

    def test_load_csv_auth(self):
        class AuthTestIO(CsvNetIO):
            url = "http://example.com/test.csv"
            username = "user"
            password = "pass"
        self.check_instance(AuthTestIO())
        headers = httpretty.last_request().headers
        auth = "Basic dXNlcjpwYXNz"  # b64encode("user:pass")
        self.assertEqual(headers.get('Authorization', None), auth)

    def test_load_csv_pickle(self):
        instance = TestIO()
        self.check_instance(instance)
        instance = pickle.loads(pickle.dumps(instance))
        self.check_instance(instance)

    def test_load_fail(self):
        class TestIO(CsvNetIO):
            url = "http://example.com/fail.txt"
        with self.assertRaises(LoadFailed) as cm:
            instance = TestIO()
        self.assertEqual(str(cm.exception), "Not Found")

    def test_load_fail_html(self):
        class TestIO(CsvNetIO):
            url = "http://example.com/fail.html"
        with self.assertRaises(LoadFailed) as cm:
            instance = TestIO()
        self.assertEqual(str(cm.exception), "Not Found")
