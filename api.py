import pandas as pd, requests, json

from preprocessing import process
from route import Route


class Api(process, Route):
    def __init__(self):
        super().__init__()

    def fetchData(self, endpoint, columns, new_columns, date):
        response = requests.get(self.URL + endpoint.format(date=date),
                                headers={'Authorization': f'Bearer {self.API_KEY}'}).json()
        df = pd.DataFrame(response)[columns]
        df.columns = new_columns
        return df

    def fetch_SMPAhead(self, date):
        smp_da = requests.get(f'https://research-api.solarkim.com/data/cmpt-2024/smp-da/{date}', headers={
            'Authorization': f'Bearer {self.API_KEY}'}).json()
        df = pd.DataFrame(smp_da)
        return df
    def fetch_Status(self, date):
        elec_supply = requests.get(f'https://research-api.solarkim.com/data/cmpt-2024/elec-supply/{date}', headers={
            'Authorization': f'Bearer {self.API_KEY}'}).json()
        df = pd.DataFrame(elec_supply)
        return df


    def get_value(self, date=''):
        data = self.fetchData('smp-da/{date}', ['ts', 'smp_da'], ['timestamp', 'price'], date)

        #x = self.fetchData('smp-rt-rc/{date}', ['ts', 'smp_rc'], ['timestamp', 'price_fir'], date)
        #data = pd.merge(data, x, on='timestamp')

        x = self.fetchData('elec-supply/{date}',
                           ['ts', 'supply_power', 'present_load', 'power_solar', 'power_wind', 'renewable_energy_total','supply_capacity', 'operation_capacity'],
                           self.STATUSNAME,
                           date)
        data = pd.merge(data, x, on='timestamp')

        data = self.standardScaler(data)
        data = self.tstodate(data)
        return data

    # def get_status(self):
    #     data = self.fetchData('smp-da/{date}', ['ts', 'smp_da'], ['timestamp', 'price'], '2024-11-04')
    #     print(data)
    def post_value(self, result):
        result = {'submit_result': result}
        print(requests.post(self.POST, data=json.dumps(result),
                            headers={'Authorization': f'Bearer {self.API_KEY}'}).json())