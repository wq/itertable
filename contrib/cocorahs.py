from wq.io import XmlNetIO
from datetime import date, timedelta

class CocorahsIO(XmlNetIO):
    state     = None
    county    = None
    startdate = date.today() - timedelta(days = 30)
    enddate   = date.today()
    type      = "Daily"

    url       = "http://data.cocorahs.org/cocorahs/export/exportreports.aspx"
    params    = {
        'dtf':            "1",
        'Format':         "XML",
        'ReportDateType': "reportdate",
        'TimesInGMT':     "False",
        'responsefields': "all"
    }
    root_tag = 'Cocorahs'
    item_tag = 'DailyPrecipReports/DailyPrecipReport'

    def load(self):
        fmt = '%m/%d/%Y'
        self.params['ReportType'] = self.type
        self.params['State']      = self.state
        if self.county is not None:
            self.params['County'] = self.county
        self.params['StartDate']  = self.startdate.strftime(fmt)
        self.params['EndDate']    = self.enddate.strftime(fmt)
        super(CocorahsIO, self).load()
