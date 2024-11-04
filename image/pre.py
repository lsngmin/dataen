import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from statsmodels.tsa.statespace.sarimax import SARIMAX, SARIMAXResults

import logging

logging.basicConfig(level=logging.INFO)

def calculate_measure(actual, forecast):
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
df1 = pd.read_csv('C:\dataen\csv\day_ahead.csv')
df2 = pd.read_csv(r'C:\dataen\csv\real_time.csv')
df3 = pd.read_csv(r'C:\dataen\csv\status.csv')

df22 = df2[['timestamp', 'price_fir']]
df33 = df3[['timestamp', 'currentDemand', 'supplyCapacity','supplyReserveCapacity','totalRenewableGeneration']]

data = df1.merge(df22, on='timestamp').merge(df33, on='timestamp')

scaler = StandardScaler()
data.loc[:, ['currentDemand', 'supplyReserveCapacity','supplyCapacity', 'totalRenewableGeneration']] = scaler.fit_transform(
data[['currentDemand', 'supplyReserveCapacity','supplyCapacity', 'totalRenewableGeneration']])


data.to_csv(r'C:\dataen\csv\total.csv', index=False)


data.loc[:, 'price_lag1'] = data['price'].shift(48)
data.loc[:, 'date_lag1'] = data['date'].shift(48)
data.loc[:, 'currentDemand_lag1'] = data['currentDemand'].shift(48)
data.loc[:, 'supplyReserveCapacity_lag1'] = data['supplyReserveCapacity'].shift(48)
data.loc[:, 'price_fir_lag1'] = data['price_fir'].shift(48)
data.loc[:, 'supplyCapacity_lag1'] = data['supplyCapacity'].shift(48)
data.loc[:, 'totalRenewableGeneration_lag1'] = data['totalRenewableGeneration'].shift(48)



index = int(data[data['timestamp'] == 1717513200].index[0]) #기존값
data = data.iloc[index:]
data.to_csv(r'C:\dataen\csv\total11.csv', index=False)
y = data['price']  # 종속 변수
x = data[['price_fir_lag1', 'currentDemand_lag1', 'supplyReserveCapacity_lag1','supplyCapacity_lag1', 'totalRenewableGeneration_lag1']]
p, d, q = 1, 1, 2
P, D, Q, m = 1, 1, 2, 48

# model = SARIMAX(y, order=(p, d, q), seasonal_order=(P, D, Q, m), exog=x)
# model_fit = model.fit(disp=True, maxiter=200, optimizer_kwargs={'options': {'disp': True}})
# model_fit.save(r'C:\dataen\model\kkk2.pkl')
# print(model_fit.summary())

model = SARIMAXResults.load(r'C:\dataen\model\kkk2.pkl')
exog = data[[ 'price_fir', 'currentDemand', 'supplyReserveCapacity', 'supplyCapacity', 'totalRenewableGeneration']].iloc[-48:-24]
forecast = model.forecast(steps=24, exog=exog)
print(forecast.tolist())
rrr = [112.58, 103.44, 102.83, 91.75, 101.85, 103.45, 106.6, 131.3, 151.13, 150.53, 145.71, 135.22, 116.31, 113.82, 114.22, 113.0, 131.17, 131.26, 131.26, 107.08, 103.42, 103.42, 103.42, 103.42]
print(calculate_measure(rrr, forecast.tolist()))

# end   = int(data[data['timestamp'] == 1730044800].index[0])
#
# data = data.iloc[index:end]
# selected_columns = ['price','price_tmp','price_fir']
# corr_matrix = data.drop(columns = ['date', 'timestamp']).corr()
# plt.figure(figsize=(12, 10))
# sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
# plt.title('Correlation Matrix')
# plt.show()

print(data.columns)

