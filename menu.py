import pandas as pd
import os

def clear_terminal():
    """Clears the terminal screen based on the operating system."""
    # Check if the operating system is Windows ('nt')
    if os.name == 'nt':
        os.system('cls')
    # Otherwise, assume it's a Unix-like system (Linux, macOS, etc.)
    else:
        os.system('clear')

def main_menu():
    clear_terminal()
    print(":: Simple Text-Based Trading UI ::")
    print("\n📈 Trading Menu (Text UI)")
    print("Select an option:")
    print("1. Market Data")
    print("2. Trading")
    print("3. Portfolio")
    print("4. Risk Management")
    print("5. Strategy Tools")
    print("6. Settings")
    print("7. Help")
    print("0. Exit")

def market_data_menu():
    clear_terminal()
    print("\n--- Market Data ---")
    print("1. View Live Prices")
    print("2. Historical Charts")
    print("3. Technical Indicators")
    print("0. Back")

def trading_menu():
    clear_terminal()
    print("\n--- Trading ---")
    print("1. Place Buy Order")
    print("2. Place Sell Order")
    print("3. Open Positions")
    print("4. Close Position")
    print("0. Back")

def portfolio_menu():
    clear_terminal()
    print("\n--- Portfolio ---")
    print("1. Account Balance")
    print("2. Current Holdings")
    print("3. Trade History")
    print("0. Back")

def risk_menu():
    print("\n--- Risk Management ---")
    print("1. Set Stop-Loss")
    print("2. Set Take-Profit")
    print("3. Diversification Report")
    print("0. Back")

def strategy_menu():
    print("\n--- Strategy Tools ---")
    print("1. Backtesting")
    print("2. Paper Trading")
    print("3. AI/ML Predictions")
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
            trading_menu()
            input("Press Enter to return...")
        elif choice == "3":
            portfolio_menu()
            input("Press Enter to return...")
        elif choice == "4":
            risk_menu()
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
