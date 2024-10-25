import pickle

import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

#종속변수의 csv
df = pd.read_csv('/Users/smin/Desktop/dataen/csv/day_ahead.csv')
#독립변수의 csv
df2 = pd.read_csv('/Users/smin/Desktop/dataen/csv/real_time.csv')
df3 = pd.read_csv('/Users/smin/Desktop/dataen/csv/status.csv')
#독립변수와 종속변수를 한 데이터프레임으로 병합
df_merge = df.merge(df2, on='timestamp').merge(df3, on='timestamp')

df_merge['timestamp'] = pd.to_datetime(df_merge['timestamp'], unit='s', utc=True)
df_merge['date'] = df_merge['timestamp'].dt.tz_convert('Asia/Seoul').dt.strftime('%Y-%m-%d %H:%M')
df_merge = df_merge[df_merge['date'] >= '2024-06-02']

df_merge['date'] = pd.to_datetime(df_merge['date'])
df_merge.set_index('date', inplace=True)
df_merge = df_merge.asfreq('h')

train_size = int(len(df_merge) * 0.8)
train = df_merge.iloc[:train_size]
test = df_merge.iloc[train_size:]


x_train, x_test = train[['price_fir', 'currentDemand', 'supplyReserveCapacity']], test[['price_fir', 'currentDemand', 'supplyReserveCapacity']]
y_train, y_test = train['price'], test['price']

def model():
    # SARIMAX 모델
    p, d, q = 1, 1, 1
    P, D, Q, m = 1, 1, 1, 168
    model = SARIMAX(y_train,
                    order=(p, d, q),
                    seasonal_order=(P, D, Q, m),
                    exog=x_train[['price_fir', 'currentDemand', 'supplyReserveCapacity']]
                    )

    model_fit = model.fit(disp=True)
    with open('/Users/smin/Desktop/dataen/model/sarimax_model.pkl', 'wb') as f:
        pickle.dump(model_fit, f)
    print(model_fit.summary())
model()