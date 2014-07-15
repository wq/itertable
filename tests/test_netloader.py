import unittest
import httpretty
from wq.io import CsvNetIO
from wq.io.exceptions import LoadFailed
import pickle


class TestIO(CsvNetIO):
    url = "http://example.com/test.csv"


class NetLoaderTestCase(unittest.TestCase):
    def setUp(self):
        httpretty.enable()
        self.data = [{
            'one': 1,
            'two': 2,
            'three': 3,
        }, {
            'one': 4,
            'two': 5,
            'three': 6,
        }]

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

    def check_instance(self, instance):
        self.assertEqual(len(instance), len(self.data))

        for row, data in zip(instance, self.data):
            for key in data:
                val = getattr(row, key)
                if isinstance(val, str) and val.isdigit():
                    val = int(val)
                self.assertEqual(val, data[key])
