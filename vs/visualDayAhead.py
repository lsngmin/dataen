import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import dataPreProcessing.tstodate as ttd



#라인 그래프
def lineplot_():
    df = pd.read_csv('/csv/day_ahead.csv')
    plt.figure(figsize=(20, 10))

    sns.lineplot(x='date', y='price', data=df, color='skyblue')

    # 그래프 제목 및 라벨 설정
    plt.title("Day-Ahead SMP")
    plt.xlabel("TIME")
    plt.xticks(ticks=range(0, len(df['date']), 250), rotation=0)  # 10개 간격으로 표시
    plt.ylabel("SMP")
    plt.grid(True)
    plt.tight_layout()  # 레이    아웃 자동 조정
    plt.show()

lineplot_()