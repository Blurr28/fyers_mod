from fyers_auth import FyersAuth
from datetime import datetime, timedelta
import pandas as pd

class Data:
    def __init__(self):
        self.resolution = "D"
        self.range_from = self._date_30_days_ago()
        self.range_to = datetime.now().strftime("%Y-%m-%d")
        self.date_format = "1"
        self.cont_flag = "1"
        self.auth = FyersAuth()
        self.fyers = self.auth.get_fyers()
        
    def _date_30_days_ago(self, delta : int = 30):
        current_date = datetime.now()
        date_30_days_ago = current_date - timedelta(days=delta)
        formatted_date = date_30_days_ago.strftime("%Y-%m-%d")
        return formatted_date

    def historical_data(self, symbol : str):

        data = {
            "symbol" : symbol, 
            "resolution" : self.resolution, 
            "date_format" : self.date_format, 
            "range_from" : self.range_from, 
            "range_to" : self.range_to, 
            "cont_flag" : self.cont_flag}
        response = self.fyers.history(data = data)
        df = pd.DataFrame(response["candles"])
        df.columns = ["datetime", "open", "high", "low", "close", "volume"]
        df["datetime"] = pd.to_datetime(df["datetime"], unit = "s")
        df["datetime"] = df["datetime"].dt.tz_localize("GMT")
        df["datetime"] = df["datetime"].dt.tz_convert("Asia/Kolkata")
        df["datetime"] = df["datetime"].dt.tz_localize(None)
        return df
    
    def set_param(self, resolution : str , range_from : str, range_to : str, date_format : str, cont_flag : str):
        if not self._check_resolution_and_date_range(resolution=resolution, range_from=range_from, range_to=range_to):
            return        
        self.resolution = resolution
        self.range_from = range_from
        self.range_to = range_to
        self.date_format = date_format
        self.cont_flag = cont_flag
        
    def _check_resolution_and_date_range(self, resolution : str, range_from : str, range_to : str) -> bool:
        resolution_available = {"5S" : 30 , "10S" : 30, "15S" : 30, "30S" : 30, "45S" : 30,
                                "1" : 100, "2" : 100, "3" : 100, "5" : 100, "10" : 100, "15" : 100,
                                "20" : 100, "30" : 100, "60" : 100, "120" : 100, "240" : 100, "D" : 366}
        if resolution not in resolution_available.keys():
            print("Error: Invalid resolution")
            print("Available resoltuons : ", resolution_available.keys())
            return False
        
        delta = datetime.strptime(range_to, "%Y-%m-%d") - datetime.strptime(range_from, "%Y-%m-%d")

        if resolution_available[resolution] < delta.days:
            print("Error : Date Range excedded")
            print(f"Maximum allowed date range for resolution {resolution} is {resolution_available[resolution]}")
            return False
        
        return True

