import pandas as pd
import requests
import json
import os
import warnings
warnings.filterwarnings('ignore')

# technical analysis
def ta_indy (symbol:str ): 
    if symbol ==   "gbpusd":
        symbol = "gbp-usd"
    elif symbol == "eurusd":
        pass
    elif symbol == "usdcad":
        symbol = "usd-cad"
    elif symbol == "usdchf":
        symbol = "usd-chf"
    elif symbol == "usdjpy":
        symbol = "usd-jpy"
    elif symbol == "audusd":
        symbol = "aud-usd"
    elif symbol == "nzdusd":
        symbol = "nzd-usd"
    elif symbol == "eurgbp":
        symbol = "eur-gbp"
    elif symbol == "gbpjpy":
        symbol = "gbp-jpy"
    
    if symbol == "eurusd":
        url = "https://www.investing.com/technical/technical-analysis"
    else :   
        url = f"https://www.investing.com/technical/{symbol}-technical-analysis"

    response = requests.get(url)
    tables = pd.read_html(response.text)
    ticker = symbol.replace("-", "").upper()

    df_pivot_points  = tables[0].copy()
    df_pivot_points  = df_pivot_points[["Name","S2","S1","Pivot Points","R1","R2"]]
    df_ta_indy = tables[1][:-1]
    df_ta_indy = df_ta_indy.replace(["Ultimate "," Power"],"", regex=True)
    df_ta_indy["Symbol"] =  ticker
    df_ma = tables[2][:-1]
    df_ma["Symbol"] =  ticker
    print("-"*59)
    print(df_ma)
    print("-"*59)
    print(df_ta_indy)
    print("-"*59)
    print(df_pivot_points)
    print("-"*59)
    return df_ma ,df_ta_indy ,df_pivot_points

