import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df1 = pd.read_csv(r'C:\dataen\csv\day_ahead.csv')
df2 = pd.read_csv(r'C:\dataen\csv\status.csv')
df3 = pd.read_csv(r'C:\dataen\csv\real_time.csv')


#하루전 전기가격과 Real-Time간의 상관관계
def aheadToRealTime() :
    merged_df = pd.merge(df1, df3, on='timestamp')
    selected_columns = ['price','price_tmp','price_fir']
    corr_matrix = merged_df[selected_columns].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.show()

#하루전 전기가격과 Status간의 상관관계
def aheadToStatus() :
    merged_df = pd.merge(df1, df2, on='timestamp')

    selected_columns = ['price', 'currentDemand', 'totalRenewableGeneration', 'supplyReserveCapacity']

    corr_matrix = merged_df[selected_columns].corr()

    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.tight_layout()
    plt.show()
aheadToRealTime()
