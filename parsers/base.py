class BaseParser(object):
    pass


class TableParser(BaseParser):
    tabular = True
    header_row = None
    max_header_row = 20
    start_row = None
    extra_data = None
