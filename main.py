from fyers_historical_data import Data

data = Data()
data.set_param("5S", "2024-09-01", "2024-10-01", "1", "1")
print(data.historical_data("NSE:SBIN-EQ", 1))