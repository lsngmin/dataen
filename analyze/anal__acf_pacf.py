import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import pandas as pd
df = pd.read_csv(r'C:\dataen\csv\status.csv')
index = int(df[df['timestamp'] == 1717340400].index[0])
df = df.iloc[index:]
plot_acf(df['supplyReserveCapacity'], lags=100)
plot_pacf(df['supplyReserveCapacity'], lags=100)
plt.show()