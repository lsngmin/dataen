import requests, json, pandas as pd, numpy as np
from matplotlib import pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX,SARIMAXResults
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import pandas as pd
import glob
import os
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# 디렉터리 경로
directory_path = r'C:\dataen\csv\weather2'

# 모든 CSV 파일 경로 가져오기
csv_files = glob.glob(os.path.join(directory_path, "*.csv"))

# 파일 이름별로 데이터프레임을 저장할 딕셔너리
df = pd.read_csv('C:\dataen\csv\기상실측데이터_1.csv')
df2 = pd.read_csv('C:\dataen\csv\기상실측데이터_2.csv')
df1 = pd.read_csv('C:\dataen\csv\day_ahead.csv')

# 각 CSV 파일을 읽어와 딕셔너리에 저장
for file_path in csv_files:
    file_name = os.path.basename(file_path).replace(".csv", "")
    #print(file_name)
    df = pd.read_csv(file_path)

    df['ts'] = pd.to_datetime(df['ts'], unit='s', errors='coerce')
    df['ts'] = df['ts'].dt.floor('h')
    df['ts'] = df['ts'].dt.tz_localize('UTC').dt.tz_convert('Asia/Seoul')
    df = df.drop_duplicates(subset='ts', keep='first').reset_index(drop=True)

    df['date'] = pd.to_datetime(df['ts'], unit='s', utc=True)
    df['date'] = df['date'].dt.tz_convert('Asia/Seoul').dt.strftime('%m-%d:%H%M')
    df['timestamp'] = df['ts'].astype('int64') // 10**9
    df.to_csv(file_path, index=False)
    merged_df = pd.merge(df1, df, on='timestamp')
    print(merged_df.columns)
# #Index(['timestamp', 'price', 'date_x', 'location', 'ts', 'temp',
#        'real_feel_temp', 'real_feel_temp_shade', 'rel_hum', 'dew_point',
#        'wind_dir', 'wind_spd', 'wind_gust_spd', 'uv_idx', 'vis', 'cld_cvr',
#        'ceiling', 'pressure', 'appr_temp', 'wind_chill_temp', 'wet_bulb_temp',
#        'precip_1h', 'date_y'],
    selected_columns = ['price', 'real_feel_temp_shade','rel_hum','wind_spd','appr_temp', 'uv_idx','temp','real_feel_temp']
    merged_df = merged_df[selected_columns]
    print(df)
    #uv_idx 이거 굿
    #real_feel_temp_shade,rel_hum,wind_dir,wind_spd,cld_cvr,appr_temp
    corr_matrix = merged_df.corr()
    # nan_rows = corr_matrix[corr_matrix.isnull().any(axis=1)]
    # print(nan_rows)
    plt.figure(figsize=(12, 10))
    #sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title(file_name + ' : Correlation Matrix')
    plt.tight_layout()
    #plt.show()

# 예: 특정 파일 데이터 확인
#print(dataframes['example_file_name'].head())  # 'example_file_name.csv' 파일의 데이터 예시



location_list = df2['location'].unique()
location_dfs = {location: df2[df2['location'] == location] for location in location_list}
# location_dfs['Sangmo-ri']['timestamp'] = location_dfs['Sangmo-ri']['ts'].astype('int64')
# location_dfs['Sangmo-ri']['date'] = pd.to_datetime(location_dfs['Sangmo-ri']['ts'], unit='s', utc=True)
# location_dfs['Sangmo-ri']['date'] = location_dfs['Sangmo-ri']['date'].dt.tz_convert('Asia/Seoul').dt.strftime('%m-%d:%H%M')

def aheadToStatus() :
    for location, data in location_dfs.items():
        path = r'C:/dataen/csv/weather2/'

        data.to_csv(path + location + '.csv', index=False)
        #data['timestamp'] = data['ts'].astype('int64')

        # merged_df = pd.merge(df1, data, on='timestamp')
        #
        # selected_columns = ['price', 'temp']
        #
        # corr_matrix = merged_df[selected_columns].corr()
        #
        # plt.figure(figsize=(12, 10))
        # sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
        # plt.title('Correlation Matrix')
        # plt.tight_layout()
        # plt.show()


# print()
# # 예시: 특정 장소의 데이터프레임 출력
# for location, data in location_dfs.items():
#     data['date'] = pd.to_datetime(data['ts'], unit='s', utc=True)
#     data['date'] = data['date'].dt.tz_convert('Asia/Seoul').dt.strftime('%m-%d:%H%M')
# df1 = df1[['ts', 'temp', 'real_feel_temp', 'real_feel_temp_shade', 'rel_hum','dew_point', 'wind_dir', 'wind_spd', 'wind_gust_spd', 'uv_idx', 'vis', 'cld_cvr', 'ceiling', 'pressure', 'appr_temp',
#        'wind_chill_temp', 'wet_bulb_temp', 'precip_1h' ]]

# df1['date'] = pd.to_datetime(df1['ts'], unit='s', utc=True)
# df1['date'] = df1['date'].dt.tz_convert('Asia/Seoul').dt.strftime('%m-%d:%H%M')
#print(df1.columns)


class Route:
    def __init__(self):
        self.API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpNzZjZTVmdG5ad1Nwc2hOc1dzS3lZIiwiaWF0IjoxNzI5NjY5NzkwLCJleHAiOjE3MzE1OTY0MDAsInR5cGUiOiJhcGlfa2V5In0.eYHCyQlrTHsg6XHS0BHEcXS03LPN8oAgyMACnkCUPCE'
        self.URL = f'https://research-api.solarkim.com/data/cmpt-2024/'
        self.POST = 'https://research-api.solarkim.com/submissions/cmpt-2024'

        self.DAYAHEAD = r'C:\dataen\csv\day_ahead.csv'
        self.REALTIME = r'C:\dataen\csv\real_time.csv'
        self.STATUS = r'C:\dataen\csv\status.csv'

        self.MODELSAVEPATH = r'C:\dataen\model\model.pkl'


class Api(Route):
    def __init__(self):
       super().__init__()
    @staticmethod
    def validparam(date):
        if date == '' :
            print("날짜 형식을 정확하게 입력하세요.")
            return exit()

    @staticmethod
    def tstodate(data):
        data['date'] = pd.to_datetime(data['timestamp'], unit='s', utc=True)
        data['date'] = data['date'].dt.tz_convert('Asia/Seoul').dt.strftime('%m-%d:%H%M')
        return data

    def get_dayahead(self, date = ''):
        self.validparam(date)
        data = pd.DataFrame(requests.get(self.URL + f'smp-da/{date}', headers={'Authorization': f'Bearer {self.API_KEY}'}).json())
        data.columns = ['timestamp', 'price']

        data = self.tstodate(data)
        csv = pd.read_csv(self.DAYAHEAD)

        n_csv = data[~data['timestamp'].isin(csv['timestamp'])]
        f_csv = pd.concat([csv, n_csv], ignore_index=True)
        f_csv.to_csv(self.DAYAHEAD, index=False, encoding='utf-8-sig')
        print(f"데이터가 기존 CSV 파일에 추가되었습니다." + date)

    def get_realtime(self, date = ''):
        self.validparam(date)
        data = pd.DataFrame(requests.get(self.URL + f'smp-rt-rc/{date}', headers={'Authorization': f'Bearer {self.API_KEY}'}).json())
        data.columns = ['timestamp', 'price_tmp', 'price_fir']

        data = self.tstodate(data)
        csv = pd.read_csv(self.REALTIME)

        n_csv = data[~data['timestamp'].isin(csv['timestamp'])]
        f_csv = pd.concat([csv, n_csv], ignore_index=True)
        f_csv.to_csv(self.REALTIME, index=False, encoding='utf-8-sig')
        print(f"데이터가 기존 CSV 파일에 추가되었습니다." + date)


    def get_status(self, date = ''):
        self.validparam(date)
        data = pd.DataFrame(requests.get(self.URL + f'elec-supply/{date}', headers={'Authorization': f'Bearer {self.API_KEY}'}).json())
        data.columns = ['timestamp', 'supplyCapacity', 'currentDemand', 'solarGeneration', 'windGeneration', 'totalRenewableGeneration', 'supplyReserveCapacity', 'operatingReserveCapacity']

        data = self.tstodate(data)
        csv = pd.read_csv(self.STATUS)

        n_csv = data[~data['timestamp'].isin(csv['timestamp'])]
        f_csv = pd.concat([csv, n_csv], ignore_index=True)
        f_csv.to_csv(self.STATUS, index=False, encoding='utf-8-sig')
        print(f"데이터가 기존 CSV 파일에 추가되었습니다." + date)

    def post_dayahead(self, result):
        result = {'submit_result' : result}
        print(requests.post(self.POST, data=json.dumps(result), headers={'Authorization': f'Bearer {self.API_KEY}'}).json())