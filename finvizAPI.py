import pandas as pd
import requests
import pytz
from datetime import datetime

# "https://finviz.com/api/forex_perf.ashx"
# "https://dd.insiad.com/currency-rates"

def now_to_inttime() :
    now= datetime.now()
    timestamp_ms = int(now.timestamp() * 1000)
    print(timestamp_ms)
    return timestamp_ms


def geturl(url:str) :
    headers = {    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    data =  response.json()
    return data



def  forex_index_perf () :
    url = "https://finviz.com/api/forex_perf.ashx"
    url1 =  "https://dd.insiad.com/currency-rates"
    headers = {    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    # Make the request with the defined headers
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data =  response.json()
        df =  pd.DataFrame.from_dict(data,"index",columns= ["value"])
        df = df.sort_values("value",ascending=False)
        return df#print(df)
    else:
        print(f"Request failed with status code: {response.status_code}")    
    return df

def forex_all_hlc () :
    url = "https://finviz.com/api/forex_all.ashx?timeframe=d"
    url = "https://finviz.com/api/forex_all.ashx?timeframe=h" #https://finviz.com/api/forex_all.ashx?timeframe=h
    url = "https://finviz.com/api/forex_all.ashx?timeframe=i15"
    url = "https://finviz.com/api/forex_all.ashx?timeframe=i5"
    #interval = "d" h i5 i15 i30 
    headers = {    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    data =  response.json()
    df = pd.DataFrame.from_dict(data,orient= "index")
    df1 = df.drop(["sparkline","sparklineDateChanges"],axis=1)
    #df = df[["label","ticker","last","change","prevClose","high","low"]]
    df1.reset_index(inplace=True, drop=True)
    print(df1)
    return df1



def ohlc_finviz (symbol:str,interval:str) :
    symbol   =  symbol.upper()
    #interval = "d" h h4 i5 i15 i30 
    now= datetime.now()
    timestamp_ms = int(now.timestamp() * 1000)
    time         = timestamp_ms
    #url = f"https://finviz.com/api/quote.ashx?aftermarket=0&barsCount=328&events=false&financialAttachments=&instrument=forex&leftBuffer=35&patterns=false&premarket=0&rev=1750517154476&ticker={symbol}&timeframe={interval}"
    url = f"https://finviz.com/api/quote.ashx?&barsCount=328&instrument=forex&rev={time}&ticker={symbol}&timeframe={interval}"
    headers = {    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    data =  response.json()
    #df = pd.DataFrame.from_dict(data,orient= "index")
    df = pd.DataFrame(data)
    df = df.dropna(axis=1)
    df = df[["ticker","timeframe","volume","date","open","high","low","close"]]
    df['date'] = pd.to_datetime(df['date'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Bangkok')
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M')
    print(df)
    try :
        return df
    except ValueError as e:
        print(f"Error: {e}")
        print("interval = d h h4 i5 i15 i30 ")
    return df

class FinvizOHLC:
    def __init__(self, symbol: str):
        self.symbol = symbol.upper()
        self.df = None

    def __str__(self):
        return str(self.df)    
    
    def _get_data(self, interval: str):
        timestamp_ms = int(datetime.now().timestamp() * 1000)
        url =    (  f"https://finviz.com/api/quote.ashx?&barsCount=328&instrument=forex"
                    f"&rev={timestamp_ms}&ticker={self.symbol}&timeframe={interval}"     )
        headers = {  'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'   )        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        df = df.dropna(axis=1)
        df = df[["ticker", "timeframe", "volume", "date", "open", "high", "low", "close"]]
        df['date'] = pd.to_datetime(df['date'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Bangkok')
        df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M')
        self.df = df
        return self
    @property
    def interval_m1(self):
        return self._get_data("i1")
    @property
    def interval_m5(self):
        return self._get_data("i5")
    @property
    def interval_m15(self):
        return self._get_data("i15")
    @property
    def interval_m30(self):
        return self._get_data("i30")
    @property
    def interval_h1(self):
        return self._get_data("h")
    @property
    def interval_h4(self):
        return self._get_data("h4")
    @property
    def interval_d1(self):
        return self._get_data("d")
    @property
    def interval_w1(self):
        return self._get_data("w")

# Uso simple

#finviz_data = FinvizOHLC("btcusd").interval_m1
#print(finviz_data) 

"""try:
    finviz_data = FinvizOHLC("btcusd").interval_m1
    print(finviz_data)  # Acceso directo al DataFrame
except ValueError as e:
    print(f"Error: {e}")
"""