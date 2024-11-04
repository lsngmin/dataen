import requests, json, pandas as pd, numpy as np, glob, os
from statsmodels.tsa.statespace.sarimax import SARIMAX,SARIMAXResults
from sklearn.preprocessing import StandardScaler
import pmdarima as pm
from pmdarima import auto_arima

class Route:
    def __init__(self):
        self.API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpNzZjZTVmdG5ad1Nwc2hOc1dzS3lZIiwiaWF0IjoxNzI5NjY5NzkwLCJleHAiOjE3MzE1OTY0MDAsInR5cGUiOiJhcGlfa2V5In0.eYHCyQlrTHsg6XHS0BHEcXS03LPN8oAgyMACnkCUPCE'
        self.URL = f'https://research-api.solarkim.com/data/cmpt-2024/'
        self.POST = 'https://research-api.solarkim.com/submissions/cmpt-2024'

        self.DAYAHEAD = r'C:\dataen\csv\day_ahead.csv'
        self.REALTIME = r'C:\dataen\csv\real_time.csv'
        self.STATUS = r'C:\dataen\csv\status.csv'

        self.MODELSAVEPATH = r'C:\dataen\model\model.pkl'


class Api(Route):
    def __init__(self):
       super().__init__()
    @staticmethod
    def validparam(date):
        if date == '' :
            print("날짜 형식을 정확하게 입력하세요.")
            return exit()

    @staticmethod
    def tstodate(data):
        data['date'] = pd.to_datetime(data['timestamp'], unit='s', utc=True)
        data['date'] = data['date'].dt.tz_convert('Asia/Seoul').dt.strftime('%m-%d:%H%M')
        return data

    def get_dayahead(self, date = ''):
        self.validparam(date)
        data = pd.DataFrame(requests.get(self.URL + f'smp-da/{date}', headers={'Authorization': f'Bearer {self.API_KEY}'}).json())
        data.columns = ['timestamp', 'price']

        data = self.tstodate(data)
        csv = pd.read_csv(self.DAYAHEAD)

        n_csv = data[~data['timestamp'].isin(csv['timestamp'])]
        f_csv = pd.concat([csv, n_csv], ignore_index=True)
        f_csv.to_csv(self.DAYAHEAD, index=False, encoding='utf-8-sig')
        print(f"데이터가 기존 CSV 파일에 추가되었습니다." + date)

    def get_realtime(self, date = ''):
        self.validparam(date)
        data = pd.DataFrame(requests.get(self.URL + f'smp-rt-rc/{date}', headers={'Authorization': f'Bearer {self.API_KEY}'}).json())
        data.columns = ['timestamp', 'price_tmp', 'price_fir']

        data = self.tstodate(data)
        csv = pd.read_csv(self.REALTIME)

        n_csv = data[~data['timestamp'].isin(csv['timestamp'])]
        f_csv = pd.concat([csv, n_csv], ignore_index=True)
        f_csv.to_csv(self.REALTIME, index=False, encoding='utf-8-sig')
        print(f"데이터가 기존 CSV 파일에 추가되었습니다." + date)


    def get_status(self, date = ''):
        self.validparam(date)
        data = pd.DataFrame(requests.get(self.URL + f'elec-supply/{date}', headers={'Authorization': f'Bearer {self.API_KEY}'}).json())
        data.columns = ['timestamp', 'supplyCapacity', 'currentDemand', 'solarGeneration', 'windGeneration', 'totalRenewableGeneration', 'supplyReserveCapacity', 'operatingReserveCapacity']

        data = self.tstodate(data)
        csv = pd.read_csv(self.STATUS)

        n_csv = data[~data['timestamp'].isin(csv['timestamp'])]
        f_csv = pd.concat([csv, n_csv], ignore_index=True)
        f_csv.to_csv(self.STATUS, index=False, encoding='utf-8-sig')
        print(f"데이터가 기존 CSV 파일에 추가되었습니다." + date)

    def get_weather(self, date=''):
        self.validparam(date)
        data = requests.get(self.URL + f'actual-weather/{date}', headers={'Authorization': f'Bearer {self.API_KEY}'}).json()
        df1 = data('2024-10-23')['actual_weather_1']
        df2 = data('2024-10-23')['actual_weather_2']
        location_list= [df1['location'].unique(),df2['location'].unique()]
        location_dfs1 = {location: df1[df1['location'] == location] for location in location_list[0]}
        location_dfs2 = {location: df2[df2['location'] == location] for location in location_list[1]}
        for location, data in location_dfs1.items():
            data['ts'] = pd.to_datetime(data['ts'], unit='s', errors='coerce')
            data['ts'] = data['ts'].dt.floor('h')
            data['ts'] = data['ts'].dt.tz_localize('UTC').dt.tz_convert('Asia/Seoul')
            data = data.drop_duplicates(subset='ts', keep='first').reset_index(drop=True)
            data['timestamp'] = data['ts'].astype('int64') // 10 ** 9
            directory_path = r'C:\dataen\csv\weather'
            csv_files = glob.glob(os.path.join(directory_path, "*.csv"))
            for file_path in csv_files:
                file_name = os.path.basename(file_path).replace(".csv", "")
                print(file_name)

                csv = pd.read_csv(file_path)
                n_csv = data[~data['timestamp'].isin(csv['timestamp'])]
                f_csv = pd.concat([csv, n_csv], ignore_index=True)
                f_csv.to_csv(file_path, index=False, encoding='utf-8-sig')

            # path = r'C:/dataen/csv/weather2/'
            # data.to_csv(path + location + '.csv', index=False)
        # data.columns = ['timestamp', 'price_tmp', 'price_fir']
        #
        # data = self.tstodate(data)
        # csv = pd.read_csv(self.REALTIME)
        #
        # n_csv = data[~data['timestamp'].isin(csv['timestamp'])]
        # f_csv = pd.concat([csv, n_csv], ignore_index=True)
        # f_csv.to_csv(self.REALTIME, index=False, encoding='utf-8-sig')
        print(f"데이터가 기존 CSV 파일에 추가되었습니다." + date)

    def post_dayahead(self, result):
        result = {'submit_result' : result}
        print(requests.post(self.POST, data=json.dumps(result), headers={'Authorization': f'Bearer {self.API_KEY}'}).json())



class PreProcessor(Route):
    def __init__(self):
        super().__init__()

        da = pd.read_csv(self.DAYAHEAD)
        rt = pd.read_csv(self.REALTIME)
        st = pd.read_csv(self.STATUS)

        data = da.merge(rt, on='timestamp').merge(st, on='timestamp')
        #df_final = data[['timestamp', 'date', 'price', 'price_fir', 'currentDemand', 'supplyReserveCapacity']].copy()
        # print(df_final.tail())

        scaler = StandardScaler()
        data.loc[:, ['currentDemand', 'supplyReserveCapacity']] = scaler.fit_transform(
        data[['currentDemand', 'supplyReserveCapacity']])

        data.loc[:, 'price_lag1'] = data['price'].shift(48)
        data.loc[:, 'date_lag1'] = data['date'].shift(48)
        data.loc[:, 'currentDemand_lag1'] = data['currentDemand'].shift(48)
        data.loc[:, 'supplyReserveCapacity_lag1'] = data['supplyReserveCapacity'].shift(48)
        data.loc[:, 'price_fir_lag1'] = data['price_fir'].shift(48)


        index = int(data[data['timestamp'] == 1717513200].index[0]) #기존값
        #index = int(data[data['timestamp'] == 1709395200].index[0]) #변경값
        self.data = data.iloc[index:]


        #print(self.data[['price_fir_lag1', 'currentDemand_lag1', 'supplyReserveCapacity_lag1']].head())
        self.y = self.data['price']  # 종속 변수
        self.x = self.data[['price_fir_lag1', 'currentDemand_lag1', 'supplyReserveCapacity_lag1']]  # 독립 변수

    def check_lateday(self):
        print("훈련에 사용될 DataFrame의 마지막 Date:" , self.data['date'].tail(1).values[0])

class SarimaxModel(PreProcessor):
    def __init__(self):
        super().__init__()
    # def auto_train(self):
    #     model = auto_arima(self.y,
    #                        exogenous=self.x,  # 독립변수
    #                        seasonal=True,  # 계절성 모델을 사용할지 여부
    #                        m=48,  # 계절 주기 (예: 하루 주기인 24)
    #                        trace=True,  # 각 단계의 로그를 출력할지 여부
    #                        error_action='ignore',  # 오류 발생 시 무시
    #                        suppress_warnings=True,  # 경고 무시
    #                        stepwise=True)  # 단계별 최적화
    #
    #     # 최적의 (p, d, q) 및 (P, D, Q, m) 출력
    #     print(model.summary())

    def train(self):
        p, d, q = 1, 1, 2
        P, D, Q, m = 1, 1, 2, 48
        model = SARIMAX(self.y, order=(p, d, q), seasonal_order=(P, D, Q, m), exog=self.x)
        model_fit = model.fit(disp=False, maxiter=200)
        model_fit.save(self.MODELSAVEPATH)
        print(model_fit.summary())
        return model_fit

    def test(self):
        pass

    def forecast(self, model = None, actual= None):
        if model is None:
            print("불러온 모델이 없어 저장된 모델을 사용합니다.")
            model = SARIMAXResults.load(self.MODELSAVEPATH)
        else:
            model = SARIMAXResults.load(model)

        exog = self.data[['price_fir', 'currentDemand', 'supplyReserveCapacity']].iloc[-48:]
        forecast = model.forecast(steps=48, exog=exog)
        if actual is None:
            print("실제값이 없어 오차율을 계산할 수 없습니다.")
            print(forecast.tolist())
            return forecast.tolist()
        print(forecast.tolist())
        print(self.calculate_measure(actual, forecast.tolist()))

    def calculate_measure(self, actual, forecast):
        actual = np.array(actual)
        forecast = np.array(forecast)

        positive_index = actual > 0
        negative_index = actual <= 0

        actual[(actual <= 0) & (actual > -1)] = -1

        n1 = np.sum(positive_index) + 1e-7
        n2 = np.sum(negative_index) + 1e-7

        e1 = (
                np.sum(
                    np.abs(actual[positive_index] - forecast[positive_index])
                    / np.abs(actual[positive_index])
                )
                / n1
        )

        e2 = (
                np.sum(
                    np.abs(actual[negative_index] - forecast[negative_index])
                    / np.abs(actual[negative_index])
                )
                / n2
        )

        TP = np.sum((forecast > 0) & (actual > 0))
        TN = np.sum((forecast <= 0) & (actual <= 0))
        FP = np.sum((forecast > 0) & (actual <= 0))
        FN = np.sum((forecast <= 0) & (actual > 0))

        Accuracy = (TP + TN) / (TP + TN + FP + FN)
        print(f'Accuracy: {Accuracy}')
        print(f'e1: {e1}, e2: {e2}')

        e_F = 0.2 * e1 + 0.8 * e2 - (Accuracy - 0.95)

        return e_F

