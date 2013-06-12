import xlrd
import datetime
import math

class WorkbookParser(object):
    workbook   = None
    worksheet  = None
    sheet_name = 0
    start_row  = None
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

        if self.start_row is None:
            self.column_count = 0
            def checkval(cell):
                if cell.value is not None and cell.value != '':
                    return True
                return False

            for row in range(5, 0, -1):
                count = len(filter(checkval, self.worksheet[row]))
                if count >= self.column_count:
                    self.column_count = count
                    self.start_row = row

        if self.field_names is None:
            row = self.worksheet[self.start_row]
            self.field_names = [c.value or 'c%s' % i for i, c in enumerate(row)]

        self.data = map(self.parse_row, self.worksheet[self.start_row+1:])

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
        def get_value(cell):
            if cell.ctype == xlrd.XL_CELL_DATE:
                time, date = math.modf(cell.value)
                tpl = xlrd.xldate_as_tuple(cell.value, self.workbook.datemode)
                if date and time:
                    return datetime.datetime(*tpl)
                elif date:
                    return datetime.date(*tpl[0:3])
                elif time:
                    return datetime.time(*tpl[3:6])

            return cell.value
        return {name: get_value(row[i])
                for i, name in enumerate(self.get_field_names())
                if i < len(row)}
