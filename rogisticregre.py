import pandas as pd

from preprocessing import process


process().defaultDataMerge()

# import pandas as pd
# from statsmodels.tsa.statespace.sarimax import SARIMAX
# import numpy as np
#
# # 데이터 로드 및 timestamp 변환
# file_path = '/Users/smin/Desktop/dataen/csv/real_time.csv'
# df = pd.read_csv(file_path)
# df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce').dt.tz_localize('UTC').dt.tz_convert('Asia/Seoul')
#
# # timestamp를 인덱스로 설정하여 시계열 데이터로 변환
# df.set_index('timestamp', inplace=True)
# df = df.asfreq('15min')
#
# # SARIMA 모델 설정 및 학습 (기본적으로 p=1, d=1, q=1 설정)
# model = SARIMAX(df['price_fir'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 24))
# sarima_result = model.fit(disp=True)
#
# # 11월 8일 00시 이후부터 11월 9일 00시까지의 데이터 예측
# end_pred = pd.Timestamp('2024-11-09 00:00:00', tz='Asia/Seoul')
# prediction = sarima_result.forecast(steps=96)
#
# # 예측된 값 출력
# print(prediction.tolist())

# target_time = pd.Timestamp('2024-11-08 00:00:00', tz='Asia/Seoul')
# end_pred = pd.Timestamp('2024-11-09 00:00:00', tz='Asia/Seoul')
# steps = int((end_pred - target_time).total_seconds() // (15 * 60))  # 15분 간격으로 예측
# timestamps = pd.date_range(start=target_time + pd.Timedelta(minutes=15), periods=steps, freq='15min', tz='Asia/Seoul').astype(int) // 10**9
# t = [103.85086517858988, 102.20581345932155, 103.3432675109533, 105.55872652968807, 107.25951042977024, 107.74879721024121, 107.46129852274915, 107.21475657780732, 112.56780756504972, 112.51765501620496, 112.50194345716852, 112.7354007253378, 112.73322805535352, 111.07706985460413, 109.80929833384879, 108.69402928403103, 108.90236971259425, 108.61855806211004, 108.13648388838493, 107.24223950088252, 105.21592159971449, 106.32398441463378, 106.74039878686735, 106.94758583690951, 104.96005535258799, 103.07211274966151, 103.99733397515335, 106.03608309511526, 107.62307101879911, 108.0631822000306, 107.76782477421997, 107.51975126562796, 112.5848857931861, 112.53317284671243, 112.51611447142626, 112.74017520905568, 112.47830860004572, 110.88075365445384, 109.65791130796913, 108.58222907222101, 108.92725927649985, 108.65351358717088, 108.1885790788242, 107.32615584722897, 105.12028666617036, 106.18890087687124, 106.59048954960205, 106.79029990919871, 104.84542905199534, 102.96613243858475, 103.89890846893195, 105.94394795370977, 107.53498669721937, 107.97684838233955, 107.68177068625262, 107.43375168399412, 112.50913542043006, 112.45747801623698, 112.44046758215428, 112.66486281490884, 112.41224075992606, 110.81259966193795, 109.58815793161781, 108.51106648887432, 108.85123082620198, 108.57712680989864, 108.11158216569281, 107.24802616824525, 105.04854863291875, 106.11856713047493, 106.5206835667427, 106.72075652091284, 104.77436707122521, 102.89476267887703, 103.82726977415248, 105.87208533524932, 107.46297987814212, 107.90477924902683, 107.60969159515344, 107.36167065258475, 112.43668953886579, 112.385030157485, 112.36801801679688, 112.59240134223258, 112.33945020068235, 110.7398833653065, 109.51549856966756, 108.43845729171207, 108.77879484360994, 108.50470358298888, 108.03918065832895, 107.17566498494948, 104.9759599205558, 106.04592842847055, 106.44802607747285, 106.64808968383166]
# predicted_values = [round(x, 2) for x in t]
#
#
# new_data = pd.DataFrame({'timestamp': timestamps, 'price_fir': predicted_values, 'price_tmp':predicted_values})
# new_data.reset_index(drop=True, inplace=True)
# df = pd.read_csv('/Users/smin/Desktop/dataen/csv/real_time.csv', index_col=None)
# df.reset_index(drop=True, inplace=True)
# df = pd.concat([df, new_data])
# df['date'] = pd.to_datetime(df['timestamp'], unit='s', utc=True)
# df['date'] = df['date'].dt.tz_convert('Asia/Seoul').dt.strftime('%m-%d:%H%M')
# df.to_csv('/Users/smin/Desktop/dataen/csv/real_time.csv')
# # 정렬하여 타임스탬프 순서대로 유지
# print(df.tail(96))