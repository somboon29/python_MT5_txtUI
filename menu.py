import pandas as pd
import config as conf
import os
from main import *
from news import *
from finvizAPI import *
from technical import *


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
    print(" [2]. Technical Analysis ")
    print(" [3]. Charting and visualizations")
    print(" [4]. News")
    print(" [5]. Market Sentiment Analysis:")
    print(" [6]. Backtesting and Strategy Development")
    print(" [7]. Deployment and Monitoring ")
    print(" [8]. Settings")
    print(" [9]. Help📚 ")
    print(" [10]. AI / ML / DL")
    print(" [0]. Exit")
    print("-"*59)

def sub_menu_news():
    while True:
        clear_terminal()
        print("📊 :: Sub Menu News ::")
        print(" [1]. Load data News")
        print(" [2]. forex News")
        print(" [3]. Gold News")
        print(" [4]. Oil News")
        print(" [0]. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("👉 Fetching Data News...")
            get_news() 
            input("Press Enter to continue...")
        elif choice == "2":
            clear_terminal()
            forex_news_table("news_forex.csv")
            input("Press Enter to continue...")
        elif choice == "3":
            clear_terminal()
            forex_news_table("news_gold.csv")
            input("Press Enter to continue...")    
        elif choice == "4":
            clear_terminal()
            forex_news_table("news_oil.csv")
            input("Press Enter to continue...")                
        elif choice == "0":
            return
        else:
            input("⚠️ Invalid choice. Press Enter to try again...")

def market_data_menu(): #1. Market Data 
    clear_terminal()
    print("\n--- Market Data ---") 
    print("1. Retrieving Historical Forex Data")
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
    print("2. Test on Historical Data")
    print("3. Vectorized vs. Event-Based")
    print("4. Robust Evaluation:")
    print("5. Risk Management")
    print("6. Optimization")
    print("7. Strategy Formulation") #[ Connect to a Trading Platform ]
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
# Data Preparation and Feature Engineering"
def run():
    while True:
        main_menu()
        choice = input("\nEnter choice: ")

        if choice == "1":
            market_data_menu()
            print("-"*59)
            df =  forex_index_perf()
            print(df)
            print("-"*59)
            input("Press Enter to return...")

        elif choice == "2":
            clear_terminal()
            print("::  Technical Forex  ::\n")
            print("Symbol list : eurusd,gbpusd,usdcad,usdchf,usdjpy,audusd\n")
            print("-"*59)
            txt = input("Press Type forex Symbol : ")
            ta_indy(txt)
            input("Press Enter to return : ")

        elif choice == "3":
            clear_terminal()
            charting_visuali_menu()
            get_news()
            print(df)
            input("Press Enter to return...")

        elif choice == "4":
            clear_terminal()
            sub_menu_news()
            #forex_news_table()
            input("Press Enter to return... ::")

        elif choice == "5":
            strategy_menu()
            get_news()
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
