import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import pandas as pd
df = pd.read_csv(r'C:\dataen\csv\day_ahead.csv')
index = int(df[df['timestamp'] == 1717340400].index[0])
df = df.iloc[index:]
rst = seasonal_decompose(df['price'], model='additive', period=168)
rst.plot()
plt.show()


