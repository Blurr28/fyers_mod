from fyers_data import Data

data = Data()
print(data.historical_data("NSE:SBIN-EQ", "D", "2024-09-01", "2024-10-01", "1", "1"))