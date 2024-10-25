import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#preprocessing
# df = pd.read_csv('/Users/smin/Desktop/dataen/csv/제주전력시장_시장전기가격_실시간가격.csv')
# df.columns = ['timestamp', 'price_tmp', 'price_fir']
# df['date'] = pd.to_datetime(df['timestamp'], unit='s', utc=True)
# df['date'] = df['date'].dt.tz_convert('Asia/Seoul').dt.strftime('%m-%d:%H%M')
# df.to_csv('/Users/smin/Desktop/dataen/csv/real_time.csv', index=False)

df = pd.read_csv('/csv/real_time.csv')
list = ['price_tmp','price_fir']
for obj in list:
    plt.figure(figsize=(20, 10))
    sns.lineplot(x='date', y=obj, data=df)
    plt.title("Real_Time : " + obj)
    plt.xlabel('Date')
    plt.xticks(ticks=range(0, len(df['date']), 250*2), rotation=0)  # 10개 간격으로 표시
    plt.ylabel(obj)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    print(obj + "'s plt ready for show")
