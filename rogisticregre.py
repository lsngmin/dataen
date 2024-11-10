import pandas as pd
import requests
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpNzZjZTVmdG5ad1Nwc2hOc1dzS3lZIiwiaWF0IjoxNzMwNzMwNzE1LCJleHAiOjE3MzE1OTY0MDAsInR5cGUiOiJhcGlfa2V5In0.V_Ky4XmSm0ykI7u4lG2OPDsy9UwHvVM3rGM1zwyuf0k'
date = '2024-10-23'

df = pd.read_csv('/Users/smin/Desktop/dataen/default/제주전력시장_시장전기가격_하루전가격.csv')

print(df)

smp_da = requests.get(f'https://research-api.solarkim.com/data/cmpt-2024/smp-da/{date}', headers={
                            'Authorization': f'Bearer {API_KEY}'}).json()
print(smp_da)
