import xlrd
import datetime
import math
from .base import TableParser


class WorkbookParser(TableParser):
    workbook = None
    worksheet = None
    sheet_name = 0
    start_row = None
    column_count = None
    no_pickle_parser = ['workbook', 'worksheet']

    def parse(self):
        self.parse_workbook()
        if self.sheet_name is None:
            self.data = [{'name': name, 'data': self.get_sheet_by_name(name)}
                         for name in self.sheet_names]
            return

        sheet_name = self.sheet_name
        if isinstance(self.sheet_name, int):
            sheet_name = self.sheet_names[sheet_name]

        self.parse_worksheet(sheet_name)

        if self.header_row is None:
            if self.start_row is not None:
                self.header_row = self.start_row - 1
            else:
                self.column_count = 0

                def checkval(cell):
                    if cell.value is not None and cell.value != '':
                        return True
                    return False

                search_rows = min(len(self.worksheet) - 1, self.max_header_row)
                for row in range(search_rows, -1, -1):
                    count = len(list(filter(checkval, self.worksheet[row])))
                    if count >= self.column_count:
                        self.column_count = count
                        self.header_row = row

        if self.start_row is None:
            self.start_row = self.header_row + 1

        if self.field_names is None:
            rows = self.worksheet[self.header_row:self.start_row]
            self.field_names = [
                str(c.value) or 'c%s' % i for i, c in enumerate(rows[0])
            ]
            for row in rows[1:]:
                for i, c in enumerate(row):
                    self.field_names[i] += "\n" + str(c.value)

            seen_fields = set()
            for i, field in enumerate(self.field_names):
                if field in seen_fields:
                    field += str(i)
                    self.field_names[i] = field
                seen_fields.add(field)

        self.data = list(map(self.parse_row, self.worksheet[self.start_row:]))

        self.extra_data = {}
        if self.header_row > 0:
            for r in range(0, self.header_row):
                for c, cell in enumerate(self.worksheet[r]):
                    val = self.get_value(cell)
                    if val is not None and val != '':
                        self.extra_data.setdefault(r, {})
                        self.extra_data[r][c] = val

    def parse_workbook(self):
        raise NotImplementedError

    @property
    def sheet_names(self):
        raise NotImplementedError

    def get_sheet_by_name(self, name):
        raise NotImplementedError

    def parse_worksheet(self, name):
        raise NotImplementedError

    def parse_row(self, row):
        raise NotImplementedError

    def get_value(self, cell):
        raise NotImplementedError

    def dump(self, file=None):
        if file is None:
            file = self.file
        write, close = self.open_worksheet(file)
        for i, field in enumerate(self.field_names):
            write(0, i, field)
        for r, row in enumerate(self.data):
            for c, field in enumerate(self.field_names):
                write(r + 1, c, row[field])
        close()


class ExcelParser(WorkbookParser):
    def parse_workbook(self):
        self.workbook = xlrd.open_workbook(file_contents=self.file.read())

    @property
    def sheet_names(self):
        return self.workbook.sheet_names()

    def get_sheet_by_name(self, name):
        return self.workbook.sheet_by_name(name)

    def parse_worksheet(self, name):
        worksheet = self.get_sheet_by_name(name)
        self.worksheet = [worksheet.row(i) for i in range(worksheet.nrows)]

    def parse_row(self, row):
        return {name: self.get_value(row[i])
                for i, name in enumerate(self.get_field_names())
                if i < len(row)}

    def get_value(self, cell):
        if cell.ctype == xlrd.XL_CELL_DATE:
            time, date = math.modf(cell.value)
            tpl = xlrd.xldate_as_tuple(cell.value, self.workbook.datemode)
            if date and time:
                return datetime.datetime(*tpl)
            elif date:
                return datetime.date(*tpl[0:3])
            else:
                return datetime.time(*tpl[3:6])
        return cell.value

    def open_worksheet(self, file):
        if getattr(self, 'filename', '').endswith('.xls'):
            import xlwt
            workbook = xlwt.Workbook()
            worksheet = workbook.add_sheet('Sheet 1')

            def close():
                workbook.save(file)
        else:
            import xlsxwriter
            workbook = xlsxwriter.Workbook(file)
            worksheet = workbook.add_worksheet()

            def close():
                workbook.close()
        return worksheet.write, close
