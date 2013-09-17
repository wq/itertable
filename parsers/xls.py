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

                for row in range(min(len(self.worksheet) - 1, 5), -1, -1):
                    count = len(filter(checkval, self.worksheet[row]))
                    if count >= self.column_count:
                        self.column_count = count
                        self.header_row = row

        if self.start_row is None:
            self.start_row = self.header_row + 1

        if self.field_names is None:
            rows = self.worksheet[self.header_row:self.start_row]
            self.field_names = [
                unicode(c.value) or u'c%s' % i for i, c in enumerate(rows[0])
            ]
            for row in rows[1:]:
                for i, c in enumerate(row):
                    self.field_names[i] += "\n" + unicode(c.value)

            seen_fields = set()
            for i, field in enumerate(self.field_names):
                if field in seen_fields:
                    field += unicode(i)
                    self.field_names[i] = field
                seen_fields.add(field)

        self.data = map(self.parse_row, self.worksheet[self.start_row:])
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
