import pandas as pd
def tstodate(uri):
    df = pd.read_csv(uri)  # 실제 파일 경로로 변경
    df['date'] = pd.to_datetime(df['ts'], unit='s', utc=True)  # UTC로 변환
    df['date'] = df['date'].dt.tz_convert('Asia/Seoul').dt.strftime('%m-%d-%H')
    df.to_csv(uri, index=False)
    return uri