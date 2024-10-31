import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

#라인 그래프
def lineplot_():
    df = pd.read_csv(r'C:\dataen\csv\day_ahead.csv')
    plt.figure(figsize=(20, 10))
    df['dates'] = pd.to_datetime(df['timestamp'], unit='s', utc=True)
    df['dates'] = df['dates'].dt.tz_convert('Asia/Seoul').dt.strftime('%m-%d')
    sns.lineplot(x='dates', y='price', data=df, color='skyblue')

    plt.title("Day-Ahead SMP")
    plt.xlabel("TIME")
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(6))  # 5 단위 간격 설정
    plt.ylabel("SMP")
    #plt.grid(True)
    plt.tight_layout()
    plt.show()

lineplot_()