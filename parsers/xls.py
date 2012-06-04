import magic

class WorkbookParser(object):
    workbook   = None
    worksheet  = None
    sheet_name = 0

    def parse(self):
        self.parse_workbook()
        
        if self.sheet_name is None:
            for name in self.sheet_names:
                self.data = {'name': name, 'data': self.get_sheet_by_name(name)}
            return
        
        sheet_name = self.sheet_name
        if isinstance(self.sheet_name, int):
            sheet_name = self.sheet_names[sheet_name]
        
        self.parse_worksheet(sheet_name)
        self.data = map(self.parse_row, self.worksheet[1:])

    def parse_workbook(self):
        raise NotImplementedError

    @property
    def sheet_names(self):
        raise NotImplementedError
    
    def get_sheet_by_name(self, name):
        raise NotImplementedError

    def parse_worksheet(self, name):
        raise NotImplementedError
    
    @property
    def column_names(self):
        raise NotImplementedError

    def parse_row(self, row):
        raise NotImplementedError

# Deal with pre-2003 format files (.xls)
class XlsParser(WorkbookParser):
    def parse_workbook(self):
        import xlrd
        self.workbook = xlrd.open_workbook(file_contents=self.file.read())

    @property
    def sheet_names(self):
        return self.workbook.sheet_names()

    def get_sheet_by_name(self, name):
        return self.workbook.sheet_by_name(name)

    def parse_worksheet(self, name):
        worksheet = self.get_sheet_by_name(name) 
        self.worksheet = [worksheet.row(i) for i in range(worksheet.nrows)]

    @property
    def column_names(self):
        row = self.worksheet[0]
        return [c.value or 'c%s' % i for i, c in enumerate(row)]

    def parse_row(self, row):
        return {name: row[i].value
                for i, name in enumerate(self.column_names)}

# Deal with 2003+ format files (.xlsx)
class XlsxParser(WorkbookParser):
    def parse_workbook(self):
        import openpyxl
        self.workbook = openpyxl.reader.excel.load_workbook(self.file, use_iterators=True)

    @property
    def sheet_names(self):
        return self.workbook.get_sheet_names()

    def get_sheet_by_name(self, name):
        return self.workbook.get_sheet_by_name(name)
    
    def parse_worksheet(self, name):
        worksheet = self.get_sheet_by_name(name) 
        self.worksheet = [row for row in worksheet.iter_rows()]

    @property
    def column_names(self):
        row = self.worksheet[0]
        return [c.internal_value or c.column for c in row]

    def parse_row(self, row):
        return {name: row[i].internal_value
                for i, name in enumerate(self.column_names)}

# Automagically determine Excel version and use appropriate parser
class ExcelParser(WorkbookParser):
    def parse(self):
        m = magic.Magic(mime=True)
        mimetype = m.from_buffer(self.file.read())
        if mimetype == 'application/vnd.ms-excel':
            cls = XlsParser
        elif mimetype == 'application/zip':
            cls = XlsxParser
        else:
            raise Exception("File does not appear to be a valid worksheet!")
        self.parser = cls()
        self.file.seek(0)
        self.parser.file = self.file
        super(ExcelParser, self).parse()

    def parse_workbook(self):
        self.parser.parse_workbook()

    @property
    def sheet_names(self):
        return self.parser.sheet_names

    def get_sheet_by_name(self, name):
        return self.parser.get_sheet_by_name(name)

    def parse_worksheet(self, name):
        self.parser.parse_worksheet(name)
        self.worksheet = self.parser.worksheet

    @property
    def column_names(self):
        return self.parser.column_names

    def parse_row(self, row):
        return self.parser.parse_row(row)
