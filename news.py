import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

df_news_forex = pd.read_csv('news_forex.csv')
df         = df_news_forex.drop(["forecast","previous"],axis=1)
df         = df[["date","country","title","impact"]]
df.columns = ["date","sym","title","impt"]
df["date"] = df["date"].str[5:16]
console = Console(width=59)
# Create a rich Panel for the main title, simulating a menu
menu_panel = Panel(
    "[bold cyan]:: forexfactory.com/calendar ::[/bold cyan]",
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

    # Convert all other values to strings to be safe
    formatted_row = [str(cell) for cell in row]
    formatted_row[3] = formatted_impact

    # Add the formatted row to the table
    table.add_row(*formatted_row)

# Print the table to the console
console.print(table)

# Print a final divider
console.print("-" * 59)