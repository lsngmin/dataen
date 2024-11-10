class Route:
    def __init__(self):
        MACPATH = r'/Users/smin/Desktop/dataen/'
        WINPATH = r'C:/dataen/'
        COLPATH = r'/content/drive/MyDrive/dataen/'

        CURPATH = MACPATH

        self.API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpNzZjZTVmdG5ad1Nwc2hOc1dzS3lZIiwiaWF0IjoxNzMwNzMwNzE1LCJleHAiOjE3MzE1OTY0MDAsInR5cGUiOiJhcGlfa2V5In0.V_Ky4XmSm0ykI7u4lG2OPDsy9UwHvVM3rGM1zwyuf0k'
        self.URL = f'https://research-api.solarkim.com/data/cmpt-2024/'
        self.POST = 'https://research-api.solarkim.com/submissions/cmpt-2024'

        self.DAYAHEAD = CURPATH + 'csv/day_ahead.csv'
        self.REALTIME = CURPATH + 'csv/real_time.csv'
        self.STATUS = CURPATH + 'csv/status.csv'

        self.MODELSAVEPATH = CURPATH + r'model/model.pkl'
        self.IMAGESAVEPATH = CURPATH + r'image/'
        self.DEFAULTCSVPATH = CURPATH + r'default/'

        self.DEFAULTCSVPATHY = CURPATH + r'default/제주전력시장_시장전기가격_하루전가격.csv'
        self.RESULTPATH = CURPATH + r'result.csv'
        self.TESTDPATH = CURPATH + r'test.csv'

        self.STATUSNAME = ['timestamp', 'supplyPower', 'presentLoad', 'powerSolar','powerWind','renewableEnergyTotal', 'supplyCapacity', 'operationCapacity']