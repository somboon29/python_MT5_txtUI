
# Copilot Instructions for AI Agents

## Project Summary
This is a Python terminal UI for Forex trading. It fetches live market data, technical analysis, and news using APIs (Finviz, Investing.com, news feeds). The UI is menu-driven and uses the `rich` library for output.

## Key Files & Roles
- `menu.py`: Entry point. Handles menu navigation and user input. Calls functions from `main.py`.
- `main.py`: Fetches news, technical indicators, and formats output with `rich`.
- `finvizAPI.py`: Gets forex OHLC and performance data from Finviz (procedural + OOP styles).
- `config.py`: API keys and config.
- `news_forex.csv`: Local news cache (used if API fails).

## How It Works
- Start with `python menu.py`.
- All data fetch/display is routed through menu options.
- Live data is fetched from APIs. If unavailable, news falls back to CSV.
- Data is processed with `pandas` and shown with `rich` (not plain `print`).

## Developer Quickstart
1. Install dependencies:
   ```sh
   pip install pandas requests rich
   ```
2. Run the app:
   ```sh
   python menu.py
   ```
3. Debug with print or `rich` console output.

## Project Conventions
- Terminal width is fixed at 59 chars for all output.
- All UI output uses `rich` (avoid plain `print` except in menus).
- API endpoints and keys are hardcoded.
- Menu navigation is a loop in `menu.py`.
- If API fails, news loads from `news_forex.csv`.

## Integration Points
- **Finviz API**: For OHLC and performance data (`finvizAPI.py`).
- **Investing.com**: For technical indicators (`main.py`).
- **News feeds**: Multiple sources, fallback to CSV.

## Usage Examples
- Fetch technical indicators for all symbols:
  ```python
  df = fetch_indicator_allsymbol()
  print(df.head(60))
  ```
- Fetch and display news:
  ```python
  df = forex_news("forex")
  print(df[["date", "title", "country"]])
  ```
- Fetch OHLC data for a symbol:
  ```python
  finviz_data = FinvizOHLC("btcusd").interval_m1
  print(finviz_data)
  ```

---
If anything is unclear or missing, please leave feedback for improvement.
