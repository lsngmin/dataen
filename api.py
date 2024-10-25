## json load 함수 정의
import requests, json
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpNzZjZTVmdG5ad1Nwc2hOc1dzS3lZIiwiaWF0IjoxNzI5NjY5NzkwLCJleHAiOjE3MzE1OTY0MDAsInR5cGUiOiJhcGlfa2V5In0.eYHCyQlrTHsg6XHS0BHEcXS03LPN8oAgyMACnkCUPCE'
date = '2024-10-23'
# 제주전력시장 시장전기가격 하루전가격 조회
def getDay_ahead(date = None, API_KEY = None):
    print(date +'\n' + API_KEY)
    if (date or API_KEY) is None:
        return print("날짜 형식 또는 API 키를 정확하게 입력하세요.")
    smp_da = requests.get(f'https://research-api.solarkim.com/data/cmpt-2024/smp-da/{date}',
                          headers={'Authorization': f'Bearer {API_KEY}'}).json()
    print("#"*8 + "!!DATA ACCESS SUCCESS!!"+ "#"*8 + "\n" + json.dumps(smp_da, ensure_ascii=False, indent=3))


getDay_ahead(date=date, API_KEY=API_KEY)