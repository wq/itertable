from wq.io import CsvNetIO
from datetime import date, timedelta

class CocorahsIO(CsvNetIO):
    state     = None
    startdate = date.today() - timedelta(days = 30)
    enddate   = date.today()
    url       = "http://data.cocorahs.org/cocorahs/export/exportreports.aspx"
    type      = "Daily"

    params    = {
        'dtf':            "1",
        'Format':         "CSV",
        'ReportDateType': "reportdate",
        'TimesInGMT':     "False"
    }

    def load(self):
        self.params['ReportType'] = self.type
        self.params['State']      = self.state
        self.params['StartDate']  = self.datef(self.startdate)
        self.params['EndDate']    = self.datef(self.enddate)
        super(CocorahsIO, self).load()

    def datef(self, date):
        return '%s/%s/%s' % (date.month, date.day, date.year)
