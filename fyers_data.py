from fyers_auth import FyersAuth

class Data:
    def __init__(self):
        self.auth = FyersAuth()
        self.fyers = self.auth.get_fyers()
    
    def historical_data(self, symbol : str, resolution : str, range_from : str, range_to : str, date_format : str = "1", cont_flag = "1"):

        data = {"symbol" : symbol, "resolution" : resolution, "date_format" : date_format, "range_from" : range_from, "range_to" : range_to, "cont_flag" : cont_flag}
        response = self.fyers.history(data = data)
        return response

        