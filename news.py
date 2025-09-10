import pandas as pd
import requests
import json
import os
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


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
        df = pd.read_csv(f"news_{source}.csv",index_col=False)
        return df
    
def get_news () :
    forex_news("forex")
    forex_news("oil")
    forex_news("gold")

def forex_news_table (source:str = "news_gold.csv") -> None:
    df_news_forex = pd.read_csv(source)
    df         = df_news_forex.drop(["forecast","previous"],axis=1)
    df         = df[["date","country","title","impact"]]
    df.columns = ["date","sym","title","impt"]
    df["date"] = df["date"].str[5:16]
    console = Console(width=59)
    # Create a rich Panel for the main title, simulating a menu
    menu_panel = Panel(
        f"[bold cyan]:: Calendar ::         source : {source} ::[/bold cyan]",
        title="[bold yellow]News Forex[/bold yellow]",
        #subtitle="[bold yellow]v1.0[/bold yellow]",
        style="bright_blue",
        border_style="dim"
    )
    console.print(menu_panel)
    table = Table( show_header=True, header_style="bold magenta", border_style="dim") #title="News Forex

    # Add columns to the table
    for col in df.columns:
        table.add_column(col)

    # Iterate over DataFrame rows and add to the table with color formatting
    for index, row in df.iterrows():
        # Format the 'impact' column based on the value
        impact_value = str(row["impt"])    #Impact
        if impact_value == "Low":
            formatted_impact = f"[yellow]{impact_value}[/yellow]"
        elif impact_value == "High":
            formatted_impact = f"[red]{impact_value}[/red]"
        elif impact_value == "Medium":
            formatted_impact = f"[orange]{impact_value}[/orange]"
        else:
            formatted_impact = impact_value
        formatted_row = [str(cell) for cell in row]
        formatted_row[3] = formatted_impact
        table.add_row(*formatted_row)

    console.print(table)
    console.print("-" * 59)