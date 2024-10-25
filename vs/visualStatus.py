import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
#preprocessing
# df = pd.read_csv('/Users/smin/Desktop/dataen/csv/제주전력시장_현황데이터.csv')
# df.columns = ['timestamp', 'supplyCapacity', 'currentDemand', 'solarGeneration', 'windGeneration', 'totalRenewableGeneration', 'supplyReserveCapacity', 'operatingReserveCapacity']
# df['date'] = pd.to_datetime(df['timestamp'], unit='s', utc=True)
# df['date'] = df['date'].dt.tz_convert('Asia/Seoul').dt.strftime('%m-%d:%H%M')
# df.to_csv('/Users/smin/Desktop/dataen/csv/status.csv', index=False)

df = pd.read_csv('/csv/status.csv')
list = ['supplyCapacity', 'currentDemand', 'solarGeneration', 'windGeneration', 'totalRenewableGeneration', 'supplyReserveCapacity', 'operatingReserveCapacity']
# for obj in list:
#     plt.figure(figsize=(20, 10))
#     sns.lineplot(x='date', y=obj, data=df)
#     plt.title("Status : " + obj)
#     plt.xlabel('Date')
#     plt.xticks(ticks=range(0, len(df['date']), 250*5), rotation=0)  # 10개 간격으로 표시
#     plt.ylabel(obj)
#     plt.grid(True)
#     plt.tight_layout()
#     plt.show()
#     print(obj + "'s plt ready for show")