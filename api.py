import pandas as pd, requests, json

from preprocessing import process
from route import Route

class Api(process, Route):
    def __init__(self):
        super().__init__()

    def fetch_SMPAhead(self, date):
        smp_da = requests.get(self.URL + f'smp-da/{date}', headers={
            'Authorization': f'Bearer {self.API_KEY}'}).json()
        return pd.DataFrame(smp_da)

    def fetch_Status(self, date):
        elec_supply = requests.get(self.URL + f'elec-supply/{date}', headers={
            'Authorization': f'Bearer {self.API_KEY}'}).json()
        return pd.DataFrame(elec_supply)


    def post_value(self, result):
        result = {'submit_result': result}
        print(requests.post(self.POST, data=json.dumps(result),
                            headers={'Authorization': f'Bearer {self.API_KEY}'}).json())