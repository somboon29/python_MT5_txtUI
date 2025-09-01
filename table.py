import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box
from rich import print
from rich.tree import Tree
from rich_tools import df_to_table

# Initialize the console with a fixed width
console = Console(width=59)

# Create a sample DataFrame
data = {
    "Stock": ["MSFT", "AAPL", "GOOGL", "AMZN", "TSLA"],
    "Price": [320.50, 175.25, 145.80, 138.90, 250.75],
    "Change": [1.55, -2.10, 0.95, -0.50, 5.25],
}
df = pd.DataFrame(data)

# Create a table object with a title
table = Table(
    title="Stock Prices",
    box=box.MINIMAL_DOUBLE_HEAD,
    header_style="bold magenta",
)

# Add columns to the table based on the DataFrame columns
table.add_column("Stock", style="cyan")
table.add_column("Price", justify="right")
table.add_column("Change", justify="right")
# Iterate through DataFrame rows and add to the table with conditional formatting
for row in df.itertuples(index=False):
    stock = row.Stock
    price = f"${row.Price:.2f}"
    change = row.Change
    
    # Conditional logic based on the 'Change' value
    if change > 0:
        change_styled = f"[bold green]+{change:.2f}[/bold green]"
    elif change < 0:
        change_styled = f"[bold red]{change:.2f}[/bold red]"
    else:
        change_styled = f"[white]{change:.2f}[/white]"

    # Add the formatted row to the rich table
    table.add_row(stock, price, change_styled)
# Print the table with dividers
print("-" * 59)
console.print(table)
print("-" * 59)    

def df_table (df) : 
    data = "news_forex.csv"
    df = pd.read_csv(data)
    table = df_to_table(df ,show_index= False)
    print(table)

def dataframe_to_rich_table(df: pd.DataFrame) -> Table:

    table = Table(title="Stock Prices",show_header=True, header_style="bold magenta" ,min_width =59 ,show_footer = True ,highlight = True)  #expand = True show_lines = True
    for col in df.columns:
        if col == "Age":
            table.add_column(col, justify="right")
        else:
            table.add_column(col, justify="left")
    # Add rows from DataFrame values converted to strings
    for _, row in df.iterrows():
        # Convert all row data elements to strings
        row_str = [str(item) for item in row]
        table.add_row(*row_str)

    return table


# Example usage
if __name__ == "__main__":
    console = Console()
    data = {
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30.2, 315.5],
        "City": ["New York", "Paris", "London"]
    }
    df = pd.DataFrame(data)

    rich_table = dataframe_to_rich_table(df)
    console.print(rich_table)
    
    """tree = Tree("Rich Tree")
    baz_tree = tree.add("baz")
    baz_tree.add("[red]Red").add("[green]Green").add("[blue]Blue")
    baz_tree.add("[red]Red").add("[green]Green")
    print(tree)"""