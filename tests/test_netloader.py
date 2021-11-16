import httpretty
from itertable import CsvNetIter, load_url
from itertable.exceptions import LoadFailed
import pickle
from .base import IterTestCase


class TestIter(CsvNetIter):
    url = "http://example.com/test.csv"


class NetLoaderTestCase(IterTestCase):
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
        self.check_instance(TestIter())

    def test_load_url(self):
        self.check_instance(load_url("http://example.com/test.csv"))

    def test_load_csv_params(self):
        self.check_instance(TestIter(params={'test': 1}))
        qs = httpretty.last_request().querystring
        self.assertEqual(qs, {'test': ['1']})

        self.check_instance(TestIter(params="test=1"))
        qs = httpretty.last_request().querystring
        self.assertEqual(qs, {'test': ['1']})

        self.check_instance(TestIter(params=None))
        qs = httpretty.last_request().querystring
        self.assertEqual(qs, {})

    def test_debug_string(self):
        instance = TestIter(debug=True)
        self.assertEqual(
            instance.debug_string, "GET: http://example.com/test.csv"
        )
        instance = TestIter(params={'test': 1}, debug=True)
        self.assertEqual(
            instance.debug_string, "GET: http://example.com/test.csv?test=1"
        )

    def test_load_csv_auth(self):
        class AuthTestIter(CsvNetIter):
            url = "http://example.com/test.csv"
            username = "user"
            password = "pass"
        self.check_instance(AuthTestIter())
        headers = httpretty.last_request().headers
        auth = "Basic dXNlcjpwYXNz"  # b64encode("user:pass")
        self.assertEqual(headers.get('Authorization', None), auth)

    def test_load_csv_pickle(self):
        instance = TestIter()
        self.check_instance(instance)
        instance = pickle.loads(pickle.dumps(instance))
        self.check_instance(instance)

    def test_load_fail(self):
        class TestIter(CsvNetIter):
            url = "http://example.com/fail.txt"
        with self.assertRaises(LoadFailed) as cm:
            TestIter()
        self.assertEqual(str(cm.exception), "Not Found")

    def test_load_fail_html(self):
        class TestIter(CsvNetIter):
            url = "http://example.com/fail.html"
        with self.assertRaises(LoadFailed) as cm:
            TestIter()
        self.assertEqual(str(cm.exception), "Not Found")
