import xlrd

class WorkbookParser(object):
    workbook   = None
    worksheet  = None
    sheet_name = 0

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

        if self.field_names is None:
            row = self.worksheet[0]
            self.field_names = [c.value or 'c%s' % i for i, c in enumerate(row)]

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
        return {name: row[i].value
                for i, name in enumerate(self.get_field_names())
                if i < len(row)}
