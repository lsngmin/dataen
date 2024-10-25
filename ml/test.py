import numpy as np
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import matplotlib.pyplot as plt
import push_data
df = pd.read_csv('/Users/smin/Desktop/dataen/csv/day_ahead.csv')
df['date'] = df['date'].apply(lambda x: pd.to_datetime(f"2024-{x}", format="%Y-%m-%d-%H", errors='coerce'))

start_date = pd.to_datetime('2024-03-01')
end_date = pd.to_datetime('2024-06-02')
df_filtered = df[(df['date'] < start_date) | (df['date'] > end_date)]

# 데이터를 학습용(train)과 테스트용(test)으로 시간 순서대로 나누기
train_size = int(len(df_filtered) * 0.8)
train, test = df_filtered[:train_size], df_filtered[train_size:]
# 데이터 정규화

# ARIMA 모델 학습 (AR(1), MA(20))
model = ARIMA(train['price'], order=(1, 1, 4))
model_fit = model.fit()

# 26일 데이터 예측 (2일 후 예측)
steps_ahead = 24  # 24시간 동안의 데이터를 예측
forecast = model_fit.forecast(steps=steps_ahead)

# 예측값을 리스트로 변환
forecast_list = forecast.tolist()
print("예측된 26일 0~24시 데이터:", forecast_list)

forecast_time_range = pd.date_range(start=pd.to_datetime('2024-10-01 00:00'), periods=steps_ahead, freq='h')

# 예측 데이터 시각화
plt.figure(figsize=(20, 10))
plt.plot(test['date'], test['price'], label='Actual')  # 실제 테스트 데이터
plt.plot(forecast_time_range, forecast, label='Forecast', linestyle='--')  # 24시간 예측
plt.legend()
plt.show()
push_data.push(forecast_list)

#plt.plot(pd.date_range(start=pd.to_datetime('2024-10-24'), periods=len(test)), test['price'], label='Actual')  # 실제 테스트 데이터
