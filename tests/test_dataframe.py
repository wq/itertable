from wq.io import load_string, BaseIO
from .base import IoTestCase


class LoadFileTestCase(IoTestCase):
    def setUp(self):
        self.csv_data = "one,two,three\n1,2,3\n4,5,6"

    def test_base_dataframe(self):
        io = BaseIO(data=self.data)
        df = io.as_dataframe()
        self.assertEqual(len(df), 2)

        val = df[df.two == 2].three[0]
        self.assertEqual(val, 3)

    def test_index_dataframe(self):
        class KeyIO(BaseIO):
            key_field = "one"

        io = KeyIO(data=self.data)
        df = io.as_dataframe()
        self.assertEqual(len(df), 2)

        val = df.ix[4].three
        self.assertEqual(val, 6)

    def test_csv_dataframe(self):
        io = load_string(self.csv_data)
        df = io.as_dataframe()
        self.assertEqual(len(df), 2)

        val = df[df.two == '2'].three[0]
        self.assertEqual(val, '3')
