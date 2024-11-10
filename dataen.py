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

from preprocessing import Api, preprocessor

#api = Api()
#api.test()
#pro = preprocessor()
# api.post_value(rsttt)
from preprocessing import process, preprocessor
#process().defaultToStatus()
#y = pd.read_csv('/Users/smin/Desktop/dataen/csv/day_ahead.csv').iloc[-24:]
# print(y)

y = pd.read_csv('/Users/smin/Desktop/dataen/csv/day_ahead.csv')['price'].iloc[-24:].tolist()

# sarimax = model.sarimax()
# s_model = sarimax.train()
# f = s_model.forecast()
# f = f[14:]
# Api().post_value(f)
# print(f)
# print(len(f))
# e1, e2, ef = model.calculateMeasure(actual=y, forecast=f)
# print(e1, ' : ', e2, ' : ', ef)
#

t = [102.65168918603956, 99.90819943493466, 94.56219279813777, 93.114435423719, 99.1883982588775, 97.95443831277808, 112.96335219061497, 116.95697099350784, 125.80998143712984, 118.03878280630448, 109.4508521158748, 98.00051975944464, 79.86304397598363, 79.30389579792305, 79.42915259377207, 76.62059477915982, 73.731352439792, 72.90271188771499, 77.62907834398135, 83.11875055166057, 87.4845156816136, 86.84582325152994, 99.63305755933483, 100.690624968466]


r = [92.32813810999718, 74.74018501893255, 72.48330592346349, 68.59191566493573, 64.517366716193, 69.23472894454335, 87.22720453361269, 92.12165911661954, 100.74818019631635, 92.73596393472312, 87.94022687197707, 72.16148583348595, 51.19335533337831, 59.416350155479705, 71.64862445070088, 81.65027964979859, 95.51966736472968, 95.28755489179069, 90.30389715304634, 92.56367705985959, 91.28107873602578, 82.15997111930244, 86.68011804039375
 , 86.05320191215479]
plt.figure()

# list1: 점선 스타일로 그리기
plt.plot(t, linestyle=':', label='forecast')

# list2: 실선 스타일로 그리기
plt.plot(r, linestyle='-', label='actual')

# 그래프 제목 및 레이블 설정
plt.title('Graph with Dotted and Solid Lines')
plt.xlabel('steps')
plt.ylabel('price')

# 범례 추가
plt.legend()

# 그래프 표시
plt.show()