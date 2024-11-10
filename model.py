import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX, SARIMAXResults
from sklearn.preprocessing import PowerTransformer

from preprocessing import preprocessor


class sarimax(preprocessor):
    def __init__(self):
        super().__init__()
        self.model = None
        self.model_fit = None

        #모델 파라미터
        self.paramNONSSN = 1, 1, 2  # p, d, q
        self.paramSSN = 1, 1, 2, 24  # P, D, Q, m
        self.method = 'powell'
        self.maxiter = 100
        # 사용할 외생변수
        self.USEEXOG = ['supplyPower', 'presentLoad', 'powerSolar', 'powerWind', 'supplyCapacity',
                        'reserve_ratio', 'demand_renewable_ratio', 'demand_supply_diff',
                        'reserve_to_demand_ratio']

        # 훈련에 사용된 마지막 일자부터 예측할 24시간 동안의 INDEX
        # EX) 11월 10일 10시 까지의 데이터를 학습시켰다면 11월 10일 11시부터 (11월 11일 1시 ~ 11월 12일 00시)까지의 데이터를 예측 해야 하므로  14+24=38
        self.USEINDEX = 38

    def train(self):
        # 모델 파라미터 설정
        p, d, q = self.paramNONSSN
        P, D, Q, m = self.paramSSN
        # cov_type='oim',  # 공분산 계산 방법 변경
        # optim_hessian='approx',  # 헤시안 계산 방식 변경
        # optim_score='harvey'
        print(f'SETTING VALUE\n NON SEASONAL(p {p}, d {d}, q {q})\n SEASONAL(P {P}, D {D}, Q {Q}, m {m})\n '
              f'MAXITER({self.maxiter}), METHOD({self.method})')

        self.model = SARIMAX(self.y, order=(p, d, q), seasonal_order=(P, D, Q, m), exog=self.x)
        self.model_fit = self.model.fit(disp=True,
                                        maxiter=self.maxiter,
                                        method=self.method

                                        )
        self.model_fit.save(self.MODELSAVEPATH)
        print(self.model_fit.summary())
        return self

    def forecast(self):
        if self.model_fit is None:
            print("저장된 모델을 사용합니다.")
            self.model_fit = SARIMAXResults.load(self.MODELSAVEPATH)

        exog = self.data[self.USEEXOG].iloc[-self.USEINDEX:]
        forecast = self.model_fit.forecast(steps=self.USEINDEX, exog=exog)

        print(forecast.tolist())

        return forecast.tolist()

    # 사용하지 않음
    def test(self):
        data = self.createTestdata()

        if self.model_fit is None:
            print("저장된 모델을 사용하여 테스트를 진행합니다.")
            self.model_fit = SARIMAXResults.load(self.MODELSAVEPATH)
        for i in range(0, len(data) - 24 + 1, 24):
            print('[' + data['date'][i:i + 24].values[0] + "] ~ [" + data['date'][i:i + 24].values[
                23] + '] 를 이용하여 예측을 수행합니다.')
            exog = data[['price_fir_lag1', 'currentDemand_lag1', 'supplyReserveCapacity_lag1',
                         'totalRenewableGeneration_lag1',
                         'supplyCapacity_lag1', 'renewable_ratio', 'reserve_ratio', 'demand_renewable_ratio',
                         'demand_supply_diff']].iloc[i:i + 24]
            y = data['price'].iloc[i:i + 24]
            forecast = self.model_fit.forecast(steps=24, exog=exog)
            e1, e2, ef = calculateMeasure(actual=y.tolist(), forecast=forecast.tolist())
            print(f'e1: {e1}, e2: {e2}\nef: {ef}')


def calculateMeasure(actual=None, forecast=None):
    if actual is None or forecast is None:
        print("값이 비어있거나 없습니다. 다시 한번 확인해주세요.")
        exit()

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
    # print(f'Accuracy: {Accuracy}')
    # print(f'e1: {e1}, e2: {e2}')

    e_F = 0.2 * e1 + 0.8 * e2 - (Accuracy - 0.95)

    return e1, e2, e_F
