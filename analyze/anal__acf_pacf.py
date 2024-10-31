import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import pandas as pd
df = pd.read_csv(r'C:\dataen\csv\day_ahead.csv')
index = int(df[df['timestamp'] == 1717340400].index[0])
df = df.iloc[index:]
plot_acf(df['price'], lags=100)
plot_pacf(df['price'], lags=100)
plt.show()