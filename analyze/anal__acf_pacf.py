import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import pandas as pd
df = pd.read_csv('/Users/smin/Desktop/dataen/csv/day_ahead.csv')
plot_acf(df['price'], lags=100)
plot_pacf(df['price'], lags=100)
plt.show()