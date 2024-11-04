import pandas as pd, os, requests, json
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta

from route import Route


class process(Route):
    def __init__(self):
        super().__init__()
        self.data = None

    def defaultDataMerge(self):
        file_paths = [
            (self.DEFAULTCSVPATHY, ['ts', '하루전가격(원/kWh)'], ['timestamp', 'price']),
            (self.DEFAULTCSVPATH + '제주전력시장_시장전기가격_실시간가격.csv', ['ts', '실시간 확정 가격(원/kWh)'], ['timestamp', 'price_fir']),
            (self.DEFAULTCSVPATH + '제주전력시장_현황데이터.csv', ['ts', '공급능력(kW)', '현재 수요(kW)', '신재생 발전량 총합(kW)', '공급 예비력(kW)'],
             ['timestamp', 'supplyCapacity', 'currentDemand', 'totalRenewableGeneration',
              'supplyReserveCapacity'])
        ]
        self.data = pd.DataFrame()
        for path, usecols, columns in file_paths:
            temp_df = pd.read_csv(path, usecols=usecols)
            temp_df.columns = columns
            self.data = temp_df if self.data.empty else pd.merge(self.data, temp_df, on='timestamp')
        self.standardScaler()
        self.tstodate()

    def standardScaler(self, data=None):
        ss = self.data if data is None else data
        except_column = ss.columns.difference(['timestamp', 'price', 'price_fir'])
        ss[except_column] = StandardScaler().fit_transform(ss[except_column])
        return ss if data is not None else setattr(self, 'data', ss)

    def tstodate(self, data=None):
        ss = self.data if data is None else data
        ss['date'] = pd.to_datetime(ss['timestamp'], unit='s', utc=True)
        ss['date'] = ss['date'].dt.tz_convert('Asia/Seoul').dt.strftime('%m-%d:%H%M')
        return ss if data is not None else setattr(self, 'data', ss)


class Api(process, Route):
    def __init__(self):
        super().__init__()

    def fetchData(self, endpoint, columns, new_columns, date):
        response = requests.get(self.URL + endpoint.format(date=date),
                                headers={'Authorization': f'Bearer {self.API_KEY}'}).json()
        df = pd.DataFrame(response)[columns]
        df.columns = new_columns
        return df

    def get_value(self, date=''):
        data = self.fetchData('smp-da/{date}', ['ts', 'smp_da'], ['timestamp', 'price'], date)

        x = self.fetchData('smp-rt-rc/{date}', ['ts', 'smp_rc'], ['timestamp', 'price_fir'], date)
        data = pd.merge(data, x, on='timestamp')

        x = self.fetchData('elec-supply/{date}',
                           ['ts', 'supply_power', 'present_load', 'renewable_energy_total', 'supply_capacity'],
                           ['timestamp', 'supplyCapacity', 'currentDemand', 'totalRenewableGeneration',
                            'supplyReserveCapacity'],
                           date)
        data = pd.merge(data, x, on='timestamp')

        data = self.standardScaler(data)
        data = self.tstodate(data)
        return data

    def post_value(self, result):
        result = {'submit_result': result}
        print(requests.post(self.POST, data=json.dumps(result),
                            headers={'Authorization': f'Bearer {self.API_KEY}'}).json())


class preprocessor(process, Route):
    def __init__(self):
        super().__init__()
        if not os.path.exists(self.RESULTPATH):
            print('PreProcessor is RUNNING...')
            self.defaultDataMerge()
            self.addApiData()
            self.data.to_csv(self.RESULTPATH)
            self.data = self.data[self.data['timestamp'] >= 1717513200]
        else:
            self.data = pd.read_csv(self.RESULTPATH)
            self.addApiData()
            self.data = self.data[self.data['timestamp'] >= 1717513200]
            self.data =self.data.reset_index(drop=True)
            self.y = self.data['price']  # 종속 변수
            self.x = self.data[
                ['price_fir_lag1', 'currentDemand_lag1', 'supplyReserveCapacity_lag1', 'totalRenewableGeneration_lag1',
                 'supplyCapacity_lag1']]  # 독립 변수


    def addApiData(self):
        end_date = datetime.strptime("2024-11-03", "%Y-%m-%d")
        start_date = self.checkLateData()
        while start_date <= end_date:
            date_str = start_date.strftime("%Y-%m-%d")
            data = Api().get_value(date_str)
            tmp_df = data[~data['timestamp'].isin(self.data['timestamp'])]
            self.data = pd.concat([self.data, tmp_df], ignore_index=True)
            start_date += timedelta(days=1)
        self.lagged_data()

    def lagged_data(self):
        lag_columns = ['price', 'currentDemand', 'supplyReserveCapacity', 'price_fir', 'totalRenewableGeneration',
                       'supplyCapacity']
        for col in lag_columns:
            self.data[f'{col}_lag1'] = self.data[col].shift(48)

    def checkLateData(self):
        lateDate = datetime.strptime(self.data['date'][-1:].values[0], "%m-%d:%H%M").replace(year=2024).strftime("%Y-%m-%d")
        return datetime.strptime(lateDate, "%Y-%m-%d")

    def createTestdata(self):
        #testData.to_csv(self.TESTDPATH)
        return self.data[self.data['timestamp'] >= 1729612800]




