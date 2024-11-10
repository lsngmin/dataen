import numpy as np
import pandas as pd, os, requests, json
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta

from route import Route
from sklearn.preprocessing import PowerTransformer


class process(Route):
    def __init__(self):
        super().__init__()
        self.data = None

    def test(self):
        df = pd.read_csv('/Users/smin/Desktop/dataen/csv/status.csv')
        df_hourly = df.iloc[::12, :].reset_index(drop=True)

        print(df_hourly)
    def defaultToStatus(self):
        df = pd.read_csv('/Users/smin/Desktop/dataen/csv/status.csv')
        data = Api().fetch_Status('2024-11-10')
        data.columns = self.STATUSNAME
        tmp_df = data[~data['timestamp'].isin(df['timestamp'])]
        df = pd.concat([df, tmp_df], ignore_index=True)
        df = self.tstodate(data=df)
        df.to_csv('/Users/smin/Desktop/dataen/csv/status.csv', index=False)

    def defaultToSMP(self):
        df = pd.read_csv('/Users/smin/Desktop/dataen/csv/day_ahead.csv')
        data = Api().fetch_SMPAhead('2024-11-09')
        data.columns = ['timestamp', 'price']
        tmp_df = data[~data['timestamp'].isin(df['timestamp'])]
        df = pd.concat([df, tmp_df], ignore_index=True)
        df = self.tstodate(data=df)
        df.to_csv('/Users/smin/Desktop/dataen/csv/day_ahead.csv', index=False)

    def defaultDataMerge(self):
        #(self.DEFAULTCSVPATH + '제주전력시장_시장전기가격_실시간가격.csv', ['ts', '실시간 확정 가격(원/kWh)'], ['timestamp', 'price_fir']),
        smp = pd.read_csv('/Users/smin/Desktop/dataen/csv/day_ahead.csv')
        status = pd.read_csv('/Users/smin/Desktop/dataen/csv/status.csv')

        self.data = pd.merge(smp, status, on='timestamp')
        self.data = self.data.drop(columns=['date_y'])
        self.data = self.data.drop(columns=['operationCapacity'])

        self.data.rename(columns={'date_x': 'date'}, inplace=True)

        self.data['reserve_ratio'] = self.data['supplyCapacity'] / self.data['supplyPower']
        self.data['demand_renewable_ratio'] = self.data['renewableEnergyTotal'] / self.data['presentLoad']
        self.data['demand_supply_diff'] = self.data['supplyPower'] - self.data['presentLoad']
        self.data['reserve_to_demand_ratio'] = self.data['supplyCapacity'] / self.data['presentLoad']
        #self.data['demand_to_supply_ratio'] = self.data['presentLoad'] / self.data['supplyPower']
        #self.data['reserve_variability'] = self.data['supplyCapacity'].diff()
        self.standardScaler()

    def standardScaler(self, data=None):
        ss = self.data if data is None else data

        # 정규화할 컬럼을 직접 선택
        normalize_columns = ['supplyPower', 'presentLoad', 'powerSolar', 'powerWind','supplyCapacity']
        ss[normalize_columns] = StandardScaler().fit_transform(ss[normalize_columns])
        # 정규화 해당 대상 제외 코드
        # except_column = ss.columns.difference(['timestamp', 'price', 'date'])
        # ss[except_column] = StandardScaler().fit_transform(ss[except_column])
        return ss if data is not None else setattr(self, 'data', ss)

    def tstodate(self, data=None):
        ss = self.data if data is None else data
        ss['date'] = pd.to_datetime(ss['timestamp'], unit='s', utc=True)
        ss['date'] = ss['date'].dt.tz_convert('Asia/Seoul').dt.strftime('%m-%d:%H%M')
        return ss if data is not None else setattr(self, 'data', ss)





class preprocessor(process, Route):
    def __init__(self):
        super().__init__()
        #if not os.path.exists(self.RESULTPATH):
        print('데이터 세트 구성중....')
        self.defaultDataMerge()
        self.data.to_csv(self.RESULTPATH)

        # #특정 시점 이후부터 학습 ( 6월 초 부터 )
        # self.data = self.data[self.data['timestamp'] >= 1717513200]
        self.data = self.data[self.data['timestamp'] >= 1717426800]#3월 4일부터17174268001709478000
        self.data = self.data[self.data['timestamp'] <= 1731200400]#11월 9일 10시까지 1731200400

        self.data = self.data.reset_index(drop=True)

        self.y = self.data['price']
        self.x = self.data[
            ['supplyPower','presentLoad','powerSolar','powerWind','supplyCapacity',
             'reserve_ratio', 'demand_renewable_ratio','demand_supply_diff',
             'reserve_to_demand_ratio']]



        # else:
        #     print('데이터 세트 추가중....')
        #     self.data = pd.read_csv(self.RESULTPATH)
        #     self.addApiData()
        #     self.lagged_data()
        #
        #     self.data = self.data[self.data['timestamp'] >= 1717513200]
        #     self.data =self.data.reset_index(drop=True)
        #
        #     self.transformer = PowerTransformer(method='yeo-johnson')
        #     self.data['yj_price'] = self.transformer.fit_transform(self.data[['price']])
        #     self.data['yj_price_lag1'] = self.data['yj_price'].shift(24)
        #     self.y = self.data['yj_price']  # 종속 변수
        #     self.x = self.data[
        #         ['yj_price_lag1', 'currentDemand_lag1', 'supplyReserveCapacity_lag1', 'totalRenewableGeneration_lag1',
        #          'supplyCapacity_lag1']]  # 독립 변수


    def addApiData(self):
        end_date = datetime.strptime("2024-11-09", "%Y-%m-%d")
        start_date = self.checkLateData()
        while start_date <= end_date:
            date_str = start_date.strftime("%Y-%m-%d")
            data = Api().get_value(date_str)
            tmp_df = data[~data['timestamp'].isin(self.data['timestamp'])]
            self.data = pd.concat([self.data, tmp_df], ignore_index=True)
            start_date += timedelta(days=1)

    def lagged_data(self):
        lag_columns = ['price', 'currentDemand', 'supplyReserveCapacity', 'totalRenewableGeneration',
                       'supplyCapacity']
        for col in lag_columns:
            self.data[f'{col}_lag1'] = self.data[col].shift(48)

    def checkLateData(self):
        lateDate = datetime.strptime(self.data['date'][-1:].values[0], "%m-%d:%H%M").replace(year=2024).strftime("%Y-%m-%d")
        return datetime.strptime(lateDate, "%Y-%m-%d")

    def createTestdata(self):
        #testData.to_csv(self.TESTDPATH)
        return self.data[self.data['timestamp'] >= 1729612800]




