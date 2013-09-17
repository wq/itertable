from wq.io import XmlNetIO
from datetime import date, timedelta


class CocorahsIO(XmlNetIO):
    state = None
    county = None
    startdate = date.today() - timedelta(days=30)
    enddate = date.today()
    datetype = "reportdate"
    type = "Daily"

    url = "http://data.cocorahs.org/cocorahs/export/exportreports.aspx"
    params = {
        'dtf': "1",
        'Format': "XML",
        'TimesInGMT': "False",
        'responsefields': "all"
    }
    root_tag = 'Cocorahs'

    @property
    def item_tag(self):
        if self.type == "Daily":
            return 'DailyPrecipReports/DailyPrecipReport'
        elif self.type == "MultiDay":
            return 'MultiDayPrecipReports/MultiDayPrecipReport'
        raise Exception("%s is not a valid report type!" % self.type)

    def load(self):
        fmt = '%m/%d/%Y'
        self.params['ReportType'] = self.type
        self.params['State'] = self.state
        if self.county is not None:
            self.params['County'] = self.county

        self.params['ReportDateType'] = self.datetype
        if self.datetype == "reportdate":
            self.params['StartDate'] = self.startdate.strftime(fmt)
            self.params['EndDate'] = self.enddate.strftime(fmt)
        elif self.datetype == "timestamp":
            self.params['Date'] = self.startdate.strftime(fmt + " %I:%M %p")

        super(CocorahsIO, self).load()
