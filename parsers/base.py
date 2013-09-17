class BaseParser(object):
    tabular = False


class TableParser(BaseParser):
    tabular = True
    header_row = None
    start_row = None
    extra_data = {}
