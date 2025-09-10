import os
import time
import math
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
"""
Forex Trading Module - Algo_trading
- โหลด config (login, password, server)
- โหลดข้อมูลจาก MetaTrader5 (MT5) -> CSV
- กลยุทธ์ (ตัวอย่าง SMA crossover + RSI)
- Backtest engine
- Grid search Optimizer
- Live Runner
- Monitor & auto-adjust
"""

try:
    import MetaTrader5 as mt5
except Exception:
    mt5 = None
# ----------------------------- Config Loader -----------------------------
def load_config(config_path: str = "test/config.json") -> Dict[str, Any]:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file {config_path} not found")
    with open(config_path, "r") as f:
        return json.load(f)

# ----------------------------- Utilities -----------------------------
def ensure_mt5_connected(config: Optional[Dict[str, Any]] = None) -> bool:
    if mt5 is None:
        raise ImportError("Install MetaTrader5 package first")
    if mt5.initialize():
        return True
    if config:
        try:
            return mt5.initialize(
                login=config.get("login"),
                password=config.get("password"),
                server=config.get("server"),
            )
        except Exception as e:
            print("MT5 init error:", e)
            return False
    return False

# --------------------------- Data loader -----------------------------
def load_mt5_data_to_csv(symbol: str, timeframe: int,
                         from_date: datetime, to_date: datetime,
                         csv_path: str, config: Optional[Dict[str, Any]]=None,
                         batch_size: int=10000) -> str:
    if not ensure_mt5_connected(config):
        raise ConnectionError("Could not initialize MT5")

    utc_from, utc_to = from_date, to_date
    all_ticks = []
    cur_to = utc_to

    while True:
        rates = mt5.copy_rates_range(symbol, timeframe, utc_from, cur_to)
        if rates is None or len(rates) == 0:
            break
        df = pd.DataFrame(rates)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        all_ticks.append(df)
        earliest = df["time"].min()
        if earliest <= utc_from or len(df) < batch_size:
            break
        cur_to = earliest - timedelta(seconds=1)

    if not all_ticks:
        raise ValueError("No data returned from MT5")

    result = (pd.concat(all_ticks, ignore_index=True)
              .drop_duplicates(subset="time")
              .sort_values("time"))
    result.to_csv(csv_path, index=False)
    print(f"Saved {len(result)} rows to {csv_path}")
    return csv_path

# ------------------------- Indicator helpers -------------------------
def sma(series: pd.Series, period: int) -> pd.Series:
    return series.rolling(period, min_periods=1).mean()

def rsi(series: pd.Series, period: int=14) -> pd.Series:
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ma_up = up.ewm(com=period - 1, adjust=False).mean()
    ma_down = down.ewm(com=period - 1, adjust=False).mean()
    rs = ma_up / (ma_down + 1e-9)
    return 100 - (100 / (1 + rs))

# --------------------------- Strategy Base ---------------------------
class Strategy:
    def __init__(self, params: Dict[str, Any]=None):
        self.params = params or {}
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

class SMARSI(Strategy):
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        fast = int(self.params.get("fast", 20))
        slow = int(self.params.get("slow", 50))
        rsi_p = int(self.params.get("rsi_period", 14))
        rsi_low = float(self.params.get("rsi_low", 30))
        rsi_high = float(self.params.get("rsi_high", 70))

        df = df.copy()
        df["sma_fast"] = sma(df["close"], fast)
        df["sma_slow"] = sma(df["close"], slow)
        df["rsi"] = rsi(df["close"], rsi_p)

        df["signal"] = 0
        df.loc[(df["sma_fast"] > df["sma_slow"]) & (df["sma_fast"].shift(1) <= df["sma_slow"].shift(1)), "signal"] = 1
        df.loc[(df["sma_fast"] < df["sma_slow"]) & (df["sma_fast"].shift(1) >= df["sma_slow"].shift(1)), "signal"] = -1

        df.loc[(df["signal"] == 1) & (df["rsi"] > rsi_high), "signal"] = 0
        df.loc[(df["signal"] == -1) & (df["rsi"] < rsi_low), "signal"] = 0

        df["position"] = df["signal"].replace(0, np.nan).ffill().fillna(0).astype(int)
        return df

# ----------------------------- Backtester ----------------------------
def backtest(df: pd.DataFrame, strategy: Strategy,
             slippage: float=0.0, fixed_size: float=0.01,
             pip_value: float=0.0001) -> Dict[str, Any]:
    data = strategy.generate_signals(df).copy()
    data["pos_change"] = data["position"].diff().fillna(0)
    trades = []
    balance = 10000.0

    for i in range(1, len(data)):
        row_prev, row = data.iloc[i - 1], data.iloc[i]
        if row["pos_change"] == 1:  # long
            entry_price = row["open"] + slippage
            trades.append({"entry_time": row["time"], "side": "long", "entry_price": entry_price,
                           "units": fixed_size})
        elif row["pos_change"] == -1:  # short
            entry_price = row["open"] - slippage
            trades.append({"entry_time": row["time"], "side": "short", "entry_price": entry_price,
                           "units": -fixed_size})

        if row["pos_change"] != 0 and trades:
            last = trades[-1]
            if "exit_time" not in last:
                exit_price = (row["open"] - slippage if last["side"] == "long"
                              else row["open"] + slippage)
                last["exit_time"] = row["time"]
                last["exit_price"] = exit_price
                last["pnl"] = (last["exit_price"] - last["entry_price"]) * (1 if last["side"]=="long" else -1) / pip_value
                balance += last["pnl"]
                last["balance_after"] = balance

    trades_df = pd.DataFrame(trades)
    performance = {"final_balance": balance,
                   "net_profit": balance - 10000.0,
                   "trade_count": len(trades_df)}
    return {"performance": performance, "trades": trades_df, "detailed": data}

# ----------------------------- Optimizer ----------------------------
def grid_optimize(df: pd.DataFrame, strategy_class,
                  param_grid: Dict[str, List[Any]],
                  metric: str="net_profit") -> Dict[str, Any]:
    import itertools
    keys = list(param_grid.keys())
    best, best_params, best_res = None, None, None
    for comb in itertools.product(*(param_grid[k] for k in keys)):
        params = dict(zip(keys, comb))
        strat = strategy_class(params)
        res = backtest(df, strat)
        score = res["performance"].get(metric, -math.inf)
        if best is None or score > best:
            best, best_params, best_res = score, params, res
    return {"best_params": best_params, "best_score": best, "result": best_res}

# ----------------------------- Deployment ----------------------------
class LiveRunner:
    def __init__(self, symbol: str, timeframe: int,
                 strategy: Strategy, config: Optional[Dict[str, Any]]=None):
        self.symbol = symbol
        self.timeframe = timeframe
        self.strategy = strategy
        self.config = config
        self.connected = ensure_mt5_connected(config)
        if not self.connected:
            raise ConnectionError("Could not connect to MT5")

    def _get_latest_bars(self, bars: int=500) -> pd.DataFrame:
        rates = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 0, bars)
        if rates is None:
            raise RuntimeError("Could not fetch rates")
        df = pd.DataFrame(rates)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        return df

    def run_once(self):
        df = self._get_latest_bars(500)
        df = self.strategy.generate_signals(df)
        last, prev = df.iloc[-1], df.iloc[-2]
        if last["position"] != prev["position"]:
            print(f"Signal changed: {prev['position']} -> {last['position']}")

    def start(self, interval_seconds: int=60):
        try:
            while True:
                self.run_once()
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("Stopped by user")

# ------------------------- Monitor & Adjust -------------------------
def monitor_performance(trades: pd.DataFrame) -> Dict[str, Any]:
    if trades.empty or "pnl" not in trades.columns:
        return {}
    wins, losses = trades[trades["pnl"] > 0], trades[trades["pnl"] <= 0]
    winrate = len(wins) / len(trades) if len(trades) else 0
    avg_win, avg_loss = wins["pnl"].mean() if not wins.empty else 0, losses["pnl"].mean() if not losses.empty else 0
    eq = trades["balance_after"].dropna().reset_index(drop=True)
    drawdown = (eq - eq.cummax())/eq.cummax() if not eq.empty else 0
    return {"total_trades": len(trades), "winrate": winrate,
            "avg_win": avg_win, "avg_loss": avg_loss,
            "max_drawdown": drawdown.min() if not isinstance(drawdown, int) else 0}

def auto_adjust(params: Dict[str, Any], stats: Dict[str, Any]) -> Dict[str, Any]:
    new = params.copy()
    if stats.get("winrate", 1) < 0.3:
        new["fixed_size"] = max(0.001, params.get("fixed_size", 0.01) * 0.7)
    elif stats.get("winrate", 1) > 0.6:
        new["fixed_size"] = min(0.1, params.get("fixed_size", 0.01) * 1.1)
    return new

# --------------------------- Example usage ---------------------------
if __name__ == "__main__":
    config = load_config("test/config.json")
    #print(config)
    symbol = "BTCUSDm"
    timeframe = mt5.TIMEFRAME_M15 if mt5 else 15
    now, start = datetime.now(), datetime.now() - timedelta(days=180)
    csvfile = f"{symbol}_m15.csv"

    if os.path.exists(csvfile):
        df = pd.read_csv(csvfile)
        df["time"] = pd.to_datetime(df["time"])
    else:
        times = pd.date_range(start=start, end=now, freq="15T")
        price = 1.10 + np.cumsum(np.random.randn(len(times)) * 0.0005)
        df = pd.DataFrame({"time": times, "open": price,
                           "high": price+0.0005, "low": price-0.0005,
                           "close": price, "tick_volume": 1})

    params = {"fast": 10, "slow": 50, "rsi_period": 14,
              "rsi_low": 30, "rsi_high": 70}
    strat = SMARSI(params)
    out = backtest(df, strat)
    print("Perf:", out["performance"])
    if not out["trades"].empty:
        stats = monitor_performance(out["trades"])
        print("Monitor:", stats)

    grid = {"fast": [ 10,8,15, 20], "slow": [35,40, 50, 89,100], "rsi_period": [14]}
    best = grid_optimize(df, SMARSI, grid)
    print("Best params:", best["best_params"], "score", best["best_score"])
    print("Done")
