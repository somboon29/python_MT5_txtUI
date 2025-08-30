import pandas as pd
import os
import tv_perf as tv

def forex_index () :
    url = "https://www.tradingview.com/markets/currencies/indices-all/"
    df = pd.read_html(url)[0]
    df["Symbol"] = df["Symbol"].str[:3]
    df = df.replace([" USD","%"],["",""] ,regex=True )
    print("-" * 59)
    print(df.to_string(index=False))
    print("-" * 59)
    return df

def print_menu():
    print("\nSelect an option:")
    print("0. Clear")
    print("1. aa")
    print("2. bb")
    print("3. cc")
    print("4. Exit")

def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "0":
            print("Clearing...")
            os.system('cls')
        elif choice == "1":
            os.system('cls')
            print( "" )
            forex_index()

        elif choice == "2":
            os.system('cls')
            print("forex_index")
            forex_index()
            tv.perf_major()

        elif choice == "3":
            print("You selected cc.")
            os.system('cls')      
            tv.perf_minor()
            
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

