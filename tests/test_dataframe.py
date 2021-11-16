from itertable import load_string, BaseIter
from .base import IterTestCase


class LoadFileTestCase(IterTestCase):
    def setUp(self):
        self.csv_data = "one,two,three\n1,2,3\n4,5,6"

    def test_base_dataframe(self):
        io = BaseIter(data=self.data)
        df = io.as_dataframe()
        self.assertEqual(len(df), 2)

        val = df[df.two == 2].three[0]
        self.assertEqual(val, 3)

    def test_index_dataframe(self):
        class KeyIter(BaseIter):
            key_field = "one"

        io = KeyIter(data=self.data)
        df = io.as_dataframe()
        self.assertEqual(len(df), 2)

        val = df.loc[4].three
        self.assertEqual(val, 6)

    def test_csv_dataframe(self):
        io = load_string(self.csv_data)
        df = io.as_dataframe()
        self.assertEqual(len(df), 2)

        val = df[df.two == '2'].three[0]
        self.assertEqual(val, '3')
