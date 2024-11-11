###   README.md
###   !!!! !!!! !!!! !!!! !!!! !!!! !!!!
###   dataen.py
###       -> Route Class : CSV file location, API information, and mapping different paths
###           -> VAR -  API_KEY : API KEY (Don't ever change it...)®
###           ->     -           URL : ROOT API URL
###           ->     -          POST : URL FOR POST
###           ->     -      DAYAHEAD : DAYAHEAD CSV FILE PATH
###           ->     -      REALTIME : REALTIME CSV FILE PATH
###           ->     -        STATUS : STATUS CSV FILE PATH
###           ->     - MODELSAVEPATH : SAVED MODEL FILE PATH
###           ->     - IMAGESAVEPATH : IMAGE FOLDER PATH
###
###
import pandas as pd
from matplotlib import pyplot as plt

import model

from preprocessing import preprocessor, process
from api import api


y = pd.read_csv('/Users/smin/Desktop/dataen/csv/day_ahead.csv')['price'].iloc[-48:-24].tolist()

sarimax = model.sarimax()
s_model = sarimax.train()
f = sarimax.forecast()

s = [102.24994065925588, 90.04058953541953, 84.82149763264722, 76.5707096909058, 75.27804770379657, 83.60830965786315, 108.14889936624442, 106.83411135477097, 114.74679151815646, 104.85131714780036, 98.76272375614664, 85.43870754981876, 73.70471761953857, 78.95061197884054, 98.41607947322468, 116.11585539566248, 128.69659287656435, 133.37118332899757, 129.42921161884468, 128.17659046058753, 124.76689422566689, 113.46291776377697, 115.6274593026227, 109.77731908647074]

# shift
e1, e2, ef = model.calculateMeasure(actual=y, forecast=f)
print(e1, ' : ', e2, ' : ', ef)

plt.figure()

# list1: 점선 스타일로 그리기
plt.plot(f, linestyle=':', label='forecast')

# list2: 실선 스타일로 그리기
plt.plot(y, linestyle='-', label='actual')

# 그래프 제목 및 레이블 설정
plt.title('Graph with Dotted and Solid Lines')
plt.xlabel('steps')
plt.ylabel('price')

# 범례 추가
plt.legend()

# 그래프 표시
plt.show()


# ff = sarimax.get_forecast()



## 불확실성 테스트

