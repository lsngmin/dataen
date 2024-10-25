import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import pandas as pd
df = pd.read_csv('/Users/smin/Desktop/dataen/csv/day_ahead.csv')
rst = seasonal_decompose(df['price'], model='additive', period=168)
rst.plot()
plt.show()