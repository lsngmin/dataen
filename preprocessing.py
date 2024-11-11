import numpy as np
import pandas as pd, os, requests, json, pytz
from sklearn.preprocessing import StandardScaler, RobustScaler
from datetime import datetime, timedelta

from route import Route
from api import api
from sklearn.preprocessing import PowerTransformer

class process(Route):
    def __init__(self):
        super().__init__()
        self.data = None
        self.robust = RobustScaler()

    def test(self):
        df = pd.read_csv('/Users/smin/Desktop/dataen/csv/status.csv')
        df_hourly = df.iloc[::12, :].reset_index(drop=True)

        print(df_hourly)
    def defaultToStatus(self):
        df = pd.read_csv('/Users/smin/Desktop/dataen/csv/status.csv')
        data = api().fetch_Status('2024-11-10')
        data.columns = self.STATUSNAME
        tmp_df = data[~data['timestamp'].isin(df['timestamp'])]
        df = pd.concat([df, tmp_df], ignore_index=True)
        df = self.tstodate(data=df)
        df.to_csv('/Users/smin/Desktop/dataen/csv/status.csv', index=False)

    def defaultToSMP(self):
        df = pd.read_csv('/Users/smin/Desktop/dataen/csv/day_ahead.csv')
        data = api().fetch_SMPAhead('2024-11-09')
        data.columns = ['timestamp', 'price']
        tmp_df = data[~data['timestamp'].isin(df['timestamp'])]
        df = pd.concat([df, tmp_df], ignore_index=True)
        df = self.tstodate(data=df)
        df.to_csv('/Users/smin/Desktop/dataen/csv/day_ahead.csv', index=False)

    def test(self, df, data):
        data.columns = ['timestamp', 'price_tmp', 'price_fir']
        tmp_df = data[~data['timestamp'].isin(df['timestamp'])]
        df = pd.concat([df, tmp_df], ignore_index=True)
        df = self.tstodate(data=df)
        return df
    def defaulttoReal(self):
        df = pd.read_csv('/Users/smin/Desktop/dataen/csv/real_time.csv')
        data = api().fetch_real('2024-11-10')
        df = self.test(df, data)

        df.to_csv('/Users/smin/Desktop/dataen/csv/real_time.csv', index=False)
        print(df)


    def defaultDataMerge(self):

        smp = pd.read_csv('/Users/smin/Desktop/dataen/csv/day_ahead.csv')
        status = pd.read_csv('/Users/smin/Desktop/dataen/csv/status.csv')
        status = status.drop(columns=['operationCapacity'])

        real = pd.read_csv('/Users/smin/Desktop/dataen/csv/real_time.csv')
        real = real.drop(columns=['date'])
        real = real.drop(columns=['price_tmp'])

        self.data = pd.merge(smp, status, on='timestamp')
        self.data = pd.merge(self.data, real, on='timestamp')

        self.data = self.data.drop(columns=['date_y'])
        self.data.rename(columns={'date_x': 'date'}, inplace=True)

        print('     데이터 병합 완료 ...')
        #self.data['reserve_ratio'] = self.data['supplyCapacity'] / self.data['supplyPower']
        #self.data['demand_renewable_ratio'] = self.data['renewableEnergyTotal'] / self.data['presentLoad']
        #self.data['demand_supply_diff'] = self.data['supplyPower'] - self.data['presentLoad']
        #self.data['reserve_to_demand_ratio'] = self.data['supplyCapacity'] / self.data['presentLoad']
        print('     파생변수 추가 완료 ...')
        print(f'        데이터의 컬럼({self.data.columns}) ...')


        #self.data['demand_to_supply_ratio'] = self.data['presentLoad'] / self.data['supplyPower']
        #self.data['reserve_variability'] = self.data['supplyCapacity'].diff()

        self.standardScaler()
        self.robustScaler()


    def robustScaler(self, data=None):
        ss = self.data if data is None else data
        print('     Robust 정규화 수행중 ...')
        # 정규화할 컬럼을 직접 선택
        columns = ['price']
        print(f'        정규화 대상 컬럼({columns})')

        ss[columns] = self.robust.fit_transform(ss[columns])
        print('     정규화 수행 완료 ...')
        print(self.data['price'])
        return ss if data is not None else setattr(self, 'data', ss)


    def standardScaler(self, data=None):
        ss = self.data if data is None else data
        print('     Standard 정규화 수행중 ...')

        # 정규화할 컬럼을 직접 선택

        normalize_columns = ['supplyPower', 'presentLoad', 'powerSolar', 'powerWind','supplyCapacity']
        print(f'        정규화 대상 컬럼({normalize_columns})')

        ss[normalize_columns] = StandardScaler().fit_transform(ss[normalize_columns])
        print('     정규화 수행 완료 ...')
        return ss if data is not None else setattr(self, 'data', ss)

    def tstodate(self, data=None):
        ss = self.data if data is None else data
        ss['date'] = pd.to_datetime(ss['timestamp'], unit='s', utc=True)
        ss['date'] = ss['date'].dt.tz_convert('Asia/Seoul').dt.strftime('%m-%d:%H%M')
        return ss if data is not None else setattr(self, 'data', ss)



class preprocessor(process, Route):
    def __init__(self):
        super().__init__()
        print('데이터 세트 구성중....')
        self.defaultDataMerge()
        print('데이터 세트를 저장합니다....')
        self.lagged_data()
        self.data.to_csv(self.RESULTPATH)

        # #특정 시점 이후부터 학습 ( 6월 초 부터 )
        start_ts = 1709391600
        end_ts = 1731164400
        korea_tz = pytz.timezone('Asia/Seoul')
        start_date = datetime.fromtimestamp(start_ts, korea_tz)
        end_date = datetime.fromtimestamp(end_ts, korea_tz)

        # 결과 출력
        print('   데이터의 시작 지점 : ' , start_date.strftime('%Y-%m-%d %H:%M:%S'))
        print('   데이터의 종료 지점 : ' , end_date.strftime('%Y-%m-%d %H:%M:%S'))

        self.data = self.data[self.data['timestamp'] >= start_ts]#3월 4일부터17174268001709478000
        self.data = self.data[self.data['timestamp'] <= end_ts]#11월 9일 10시까지 1731200400

        self.data = self.data.reset_index(drop=True)
        #print(self.data.tail(48))
        self.y = self.data['price']
        self.x = self.data[
            ['presentLoad','supplyCapacity','price_fir', 'powerSolar', 'powerWind']]
        #'reserve_ratio_lag', 'demand_renewable_ratio_lag','demand_supply_diff_lag', 'reserve_to_demand_ratio_lag',

    # def addApiData(self):
    #     end_date = datetime.strptime("2024-11-09", "%Y-%m-%d")
    #     start_date = self.checkLateData()
    #     while start_date <= end_date:
    #         date_str = start_date.strftime("%Y-%m-%d")
    #         data = Api().get_value(date_str)
    #         tmp_df = data[~data['timestamp'].isin(self.data['timestamp'])]
    #         self.data = pd.concat([self.data, tmp_df], ignore_index=True)
    #         start_date += timedelta(days=1)

    def lagged_data(self):
        lag_columns =  ['supplyPower','presentLoad','powerSolar','powerWind','supplyCapacity',
              'price_fir']
        #'reserve_ratio', 'demand_renewable_ratio','demand_supply_diff', 'reserve_to_demand_ratio',
        self.data['date_lag'] = self.data['date'].shift(48)
        for col in lag_columns:
            self.data[f'{col}_lag'] = self.data[col].shift(48)
            print(f'{col}의 데이터 shift의 성공했습니다.')

    def checkLateData(self):
        lateDate = datetime.strptime(self.data['date'][-1:].values[0], "%m-%d:%H%M").replace(year=2024).strftime("%Y-%m-%d")
        return datetime.strptime(lateDate, "%Y-%m-%d")

    def createTestdata(self):
        #testData.to_csv(self.TESTDPATH)
        return self.data[self.data['timestamp'] >= 1729612800]




