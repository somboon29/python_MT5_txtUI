import pandas as pd
import config as conf
import os
from main import *

def clear_terminal():
    # Check if the operating system is Windows ('nt')
    os.system('cls' if os.name == 'nt' else 'clear') 
    """if os.name == 'nt':
        os.system('cls')
    else:
        os.system('cls')"""

def main_menu():
    clear_terminal()
    print("-"*59)
    print("📈 Forex Trading Menu (Text UI)")
    print("-"*59)
    print("Select an option:")
    print(" [1]. Market Data")
    print(" [2]. Analysis Trading")
    print(" [3]. Charting and visualizations")
    print(" [4]. News")
    print(" [5]. Strategy Optimisation")
    print(" [6]. Data-driven market analysis")
    print(" [7]. AI Chat")
    print(" [8]. Settings")
    print(" [9]. Help📚 ")
    print(" [0]. Exit")
    
    print("-"*59)

def market_data_menu(): #1. Market Data 
    clear_terminal()
    print("\n--- Market Data ---")
    print("1. View Live Prices")
    print("2. Historical Charts")
    print("3. Technical Indicators")
    print("0. Back")

def analysis_trading_menu():
    clear_terminal()
    print("-"*59)
    print(":: --- Singnal Trading ---::")
    print("-"*59)
    print("1. Technical Analysis")
    print("2. Sentiment Analysis")
    print("0. Back")
    print("-"*59)

def portfolio_menu():
    clear_terminal()
    print("\n--- Portfolio ---")
    print("1. Account Balance")
    print("2. Current Holdings")
    print("3. Trade History")
    print("0. Back")

def charting_visuali_menu(): #3. 
    clear_terminal()
    print("::--- Charting and visualizations --::")
    print("1. Dsashboard")
    print("2. Barchart")
    print("3. Diversification Report")
    print("0. Back")

def strategy_menu(): #  Parameter Optimisation
    clear_terminal()
    print(":: --- Strategy Tools --- ::")
    print("1. Backtesting")
    print("2. Paper Trading")
    print("3. AI/ML Predictions")
    print("4. Strategy Optimisation")
    print("5. Parameter Optimisation")
    print("0. Back")

def settings_menu():
    print("\n--- Settings ---")
    print("1. Configure Broker API")
    print("2. Update Trading Preferences")
    print("3. Notifications")
    print("0. Back")

def help_menu():
    print("\n--- Help ---")
    print("1. User Guide")
    print("2. Contact Support")
    print("0. Back")

# Navigation loop
def run():
    while True:
        main_menu()
        choice = input("\nEnter choice: ")

        if choice == "1":
            market_data_menu()
            input("Press Enter to return...")

        elif choice == "2":
            analysis_trading_menu()  
            clear_terminal()
            print("-"*59)   
            df  = fetch_indicator_allsymbol()
            print(df.head(60))
            print("-"*59) 
            print(df.tail(60))
            print("-"*59)  
            input("Press Enter to return : ")

        elif choice == "3":
            charting_visuali_menu()
            input("Press Enter to return...")

        elif choice == "4":
            clear_terminal()
            df = forex_news("forex")
            df = df[["date","title","country"]]
            df["date"] = df["date"].str[5:16]
            print("-"*59) 
            print(df.to_string(index=False)
            print("-"*59) 
              
            input("Press Enter to return...")

        elif choice == "5":
            strategy_menu()
            input("Press Enter to return...")
        elif choice == "6":
            settings_menu()
            input("Press Enter to return...")

        elif choice == "7":
            help_menu()
            input("Press Enter to return...")

        elif choice == "0":
            print("\nExiting Trading Console. Goodbye! 👋")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    run()
