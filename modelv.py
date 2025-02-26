import requests
from datetime import datetime, timedelta
import config

class UserModel:
    def __init__(self):
        self.apikey = config.APIKEY
        self.basepoint = "https://financialmodelingprep.com/api/v3/stock/list"
    def request(self):
        params = {
            "format": "json"
            }
        url = f"{self.basepoint}?apikey={self.apikey}"
        return requests.get(url,params=params)
    def getdata(self,ticker):
        response = self.request()

        stockinfo = response.json()

        for stock in stockinfo:
            if stock["symbol"] == ticker:
                stockd = stock
                stockd["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return stockd
        
