import pandas as pd, seaborn as sns
from matplotlib import pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from route import Route

class Analyze(Route):
    def __init__(self):
        super().__init__()
        df = pd.read_csv(self.DAYAHEAD)
        index = int(df[df['timestamp'] == 1717340400].index[0])
        self.df = df.iloc[index:]
        self.ahead = pd.read_csv(self.DAYAHEAD)
        self.status = pd.read_csv(self.STATUS)
        self.realtime = pd.read_csv(self.REALTIME)

    def anal_acf(self, lags=100):
        plot_acf(self.df['price'], lags=lags)
        plt.show()
        plt.imsave(self.IMAGESAVEPATH + 'acf.png')

    def anal_pacf(self, lags=100):
        plot_pacf(self.df['price'], lags=lags)
        plt.show()
        plt.imsave(self.IMAGESAVEPATH + 'pacf.png')

    def anal_decompose(self, period=24):
        rst = seasonal_decompose(self.df['price'], model='additive', period=period)
        rst.plot()
        plt.show()
        plt.imsave(self.IMAGESAVEPATH + 'decompose.png')

    def anal_corr_matrix_status(self):
        merged_df = pd.merge(self.ahead, self.status, on='timestamp')

        columns = ['price', 'currentDemand', 'totalRenewableGeneration', 'supplyReserveCapacity','totalRenewableGeneration','supplyCapacity']

        corr_matrix = merged_df[columns].corr()

        plt.figure(figsize=(12, 10))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
        plt.title('Correlation Matrix')
        plt.tight_layout()
        plt.show()
        plt.imsave(self.IMAGESAVEPATH + 'corr_matrix_stat.png')

    def anal_corr_matrix_realtime(self):
        merged_df = pd.merge(self.ahead, self.realtime, on='timestamp')
        columns = ['price', 'price_tmp', 'price_fir']
        corr_matrix = merged_df[columns].corr()
        plt.figure(figsize=(8, 6))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
        plt.title('Correlation Matrix')
        plt.show()
        plt.imsave(self.IMAGESAVEPATH + 'corr_matrix_rt.png')