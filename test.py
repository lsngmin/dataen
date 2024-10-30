from dataen import Route, PreProcessor, SarimaxModel

pp = PreProcessor()
sarimax = SarimaxModel()
actual = [101.81, 76.9, 77.3, 78.08, 99.38, 87.14, 100.42, 109.13, 139.31, 117.02, 116.97, 109.93, 100.4, 100.58, 110.68, 109.06, 116.86, 117.02, 117.12, 116.32, 117.33, 100.89, 116.03, 111.96]
sarimax.calculate_measure(actual, sarimax.forecast(sarimax.train()))

