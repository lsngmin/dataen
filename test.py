from dataen import Route, PreProcessor, SarimaxModel, Api
api = Api()
sarimax = SarimaxModel()
# actual = [101.81, 76.9, 77.3, 78.08, 99.38, 87.14, 100.42, 109.13, 139.31, 117.02, 116.97, 109.93, 100.4, 100.58, 110.68, 109.06, 116.86, 117.02, 117.12, 116.32, 117.33, 100.89, 116.03, 111.96]
rst = [103.72639157391217, 100.28131733506069, 89.52522080635298, 74.68381317041758, 78.59937749665676, 90.28015388040606, 114.43823525973818, 117.88323729897354, 131.16213680486433, 129.620398993947, 112.26856719477485, 105.77935325223483, 98.05987821082945, 107.88778570688292, 120.87407960003372, 128.8255265019535, 128.96027754174847, 137.16764760618346, 141.08778210314955, 142.5175576825981, 139.20577271247546, 125.44871384409421, 131.42089008394416, 124.86044788655168]
sss = [106.209618976626, 98.91763071060134, 92.03428718813436, 74.48927868156781, 78.45099813507287, 89.9119783401809, 114.55922011805444, 115.21465860881138, 130.00457648531525, 128.82175460842686, 112.77519952724529, 107.501881673447, 100.71707471952965, 109.07753939708086, 120.9167839503672, 128.19092843768567, 128.54638564571326, 136.21953342848641, 138.71125635471716, 139.53691264496845, 136.36467949534793, 122.08587471239711, 127.16408569786218, 120.78345773556687]

api.post_dayahead(sarimax.forecast(sarimax.train()))