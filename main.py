import pandas as pd
import requests
import json
import os
from finvizAPI  import *
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.live import Live
from rich.align import Align
import warnings
warnings.filterwarnings('ignore')

# --- Configuration: Set terminal width to 59 characters ---
MAX_WIDTH = 59
console = Console(width=MAX_WIDTH)

NEWS_HEADLINES = [
    "Fed holds interest rates steady, citing moderate economic growth.",
    "ECB President hints at potential policy shifts in the coming quarter.",
    "Global supply chain disruptions continue to impact manufacturing output.",
    "Tech stocks surge on positive earnings reports from major players.",
    "Oil prices climb as geopolitical tensions rise."  ]

def print_divider():
    """Prints the separator line of 59 characters."""
    console.print("-" * MAX_WIDTH)

def forex_news(source = "forex"):
    if source == "cypto" :
        url = "https://nfs.faireconomy.media/cc_calendar_thisweek.json"
    elif   source == "oil" :  
        url = "https://nfs.faireconomy.media/ee_calendar_thisweek.json"
    elif   source == "gold" :  
        url = "https://nfs.faireconomy.media/mm_calendar_thisweek.json"    
    else   :   
        url= "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
    try :
        url     = requests.get (url)
        data    = json.loads(url.text)
        df      = pd.json_normalize(data)
        df["date"] = df["date"].str[:16].str.replace("T"," ")
        df.to_csv( f"news_{source}.csv", index= False)
        #print(df)
        return df
    except ValueError as e:
        print(f"Error: {e}")
        print("exceeded the limit for Calendar  Please wait")
        df = pd.read_csv(f"forex_txtui/news_forex.csv",index_col=False)
        return df

 
 
def show_news():
    """Displays formatted news headlines in a panel."""
    os.system('cls' if os.name == 'nt' else 'clear')
    news_content = Text()
    for i, headline in enumerate(NEWS_HEADLINES, 1):
        news_content.append(f": {i}. {headline}\n\n")

    console.print(
        Panel(
            news_content,
            title="[bold green]📰 Latest News[/]",
            border_style="green",
            padding=(1, 2)
        )
    )


def fetch_indicator_allsymbol(symbols: list[str] = None) -> pd.DataFrame:
    SYMBOL_TABLE_MAP = {
    0: "EURUSD", 3: "GBPUSD", 6: "USDJPY",
    9: "CHFUSD", 12: "AUDUSD", 15: "EURGBP",
    18: "USDCAD", 21: "NZDUSD"  }

    url = "https://www.investing.com/technical/indicators"
    response = requests.get(url)
    tables = pd.read_html(response.text)

    result_frames = []
    for idx, symbol in SYMBOL_TABLE_MAP.items():
        if (symbols is None) or (symbol in symbols):
            df1 = tables[idx]
            df2 = tables[idx + 1]
            df = pd.concat([df1, df2], ignore_index=True)
            df["symbol"] = symbol
            df = df[["symbol", "Name", "Value", "Action"]]
            result_frames.append(df)

    df = pd.concat(result_frames, ignore_index=True)
    return df


def ta_indy (symbol:str = "eurusd"):
    if symbol ==   "gbpusd":
        symbol = "gbp-usd"
    elif symbol == "eurusd":
        symbol = "eur-usd"
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
    
    url = f"https://www.investing.com/technical/{symbol}-technical-analysis"
    response = requests.get(url)
    tables = pd.read_html(response.text)
    ticker = symbol.replace("-", "").upper()

    df_pivot_points  = tables[0]
    df_ta_indy = tables[1][:-1]
    df_ta_indy = df_ta_indy.replace(["Ultimate "," Power"],"", regex=True)
    df_ta_indy["Symbol"] =  ticker
    df_ma = tables[2][:-1]
    df_ma["Symbol"] =  ticker
    #print(df_pivot_points)
    print(df_ta_indy)
    print(df_ma)
    return df_ma ,df_ta_indy ,df_pivot_points

def emoji () :
    print("📊","📈","🔴","📌","🌈","🚨","⏳","🚧","🚩","🏁","📅","🔛","🔜")
    print("🕛","🆚","💹","➖","✅","✔️","💲","🔰","⚠️","🚦","🔔","🔕")
    print("◀️","▶️","⬇️","⬆️","⚡️","🔒️","🔐")
    import rich
    rich.print(":red_circle:")
    rich.print(":rocket:")
    rich.print(":star2:")
    rich.print(":collision:")
    rich.print(":fire:")
    rich.print(":yen:")
    rich.print(":ledger:")    #:closed_book:  :green_book: :ledger: green_book ::books::
    rich.print(":bar_chart:")
    rich.print(":pushpin: 12345 :bar_chart:")