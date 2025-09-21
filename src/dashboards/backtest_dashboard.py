import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from src.signal_engine import SignalEngine

st.title("📊 Quant-Agent Backtest Dashboard")

def backtest_strategy(ticker, start, end, benchmark="SPY"):
    engine = SignalEngine()
    data = engine.compute_indicators(ticker, start=start, end=end)
    if data.empty:
        raise ValueError(f"No data available for {ticker} between {start} and {end}")

    df = pd.DataFrame(index=data.index)
    df["Close"] = data["Close"]

    # === Strategy Rule ===
    df["signal"] = np.where(data["SMA20"] > data["SMA50"], "BUY", "SELL")
    df["Return"] = df["Close"].pct_change().fillna(0)
    df["SignalReturn"] = df["Return"] * df["signal"].map({"BUY": 1, "SELL": -1})
    df["Equity"] = (1 + df["SignalReturn"]).cumprod()

    # === Benchmark ===
    bench = yf.download(benchmark, start=start, end=end)["Close"].pct_change().fillna(0)
    benchmark_equity = (1 + bench).cumprod()

    # === Metrics ===
    total_return = df["Equity"].iloc[-1] - 1
    annual_return = (1 + total_return) ** (252 / len(df)) - 1
    sharpe = np.mean(df["SignalReturn"]) / (np.std(df["SignalReturn"]) + 1e-6) * np.sqrt(252)
    max_dd = (df["Equity"].cummax() - df["Equity"]).max()

    trades = df["signal"].ne(df["signal"].shift()).sum()
    wins = (df["SignalReturn"] > 0).sum()
    win_rate = wins / trades if trades > 0 else 0
    avg_pnl = df["SignalReturn"].mean()

    # === Trade Log ===
    trade_log = []
    position = None
    entry_price = 0
    for i in range(1, len(df)):
        if df["signal"].iloc[i] == "BUY" and position is None:
            position = "LONG"
            entry_price = df["Close"].iloc[i]
            entry_date = df.index[i]
        elif df["signal"].iloc[i] == "SELL" and position == "LONG":
            exit_price = df["Close"].iloc[i]
            pnl = (exit_price - entry_price) / entry_price
            trade_log.append({"Entry": entry_date, "Exit": df.index[i], "PnL": round(pnl * 100, 2)})
            position = None

    trade_log = pd.DataFrame(trade_log)

    return df, benchmark_equity, total_return, annual_return, sharpe, max_dd, trades, win_rate, avg_pnl, trade_log


ticker = st.text_input("Enter ticker:", "TSLA")
start_date = st.date_input("Start date", pd.to_datetime("2022-01-01"))
end_date = st.date_input("End date", pd.to_datetime("2023-01-01"))

if st.button("Run Backtest"):
    try:
        df, benchmark_equity, total_return, annual_return, sharpe, max_dd, trades, win_rate, avg_pnl, trade_log = backtest_strategy(
            ticker, start_date, end_date
        )

        # === Metrics ===
        st.subheader(f"Backtest Results for {ticker}")
        st.json({
            "Total Return %": round(total_return * 100, 2),
            "Annual Return %": round(annual_return * 100, 2),
            "Sharpe Ratio": round(sharpe, 2),
            "Max Drawdown %": round(max_dd * 100, 2),
            "Trades": int(trades),
            "Win Rate %": round(win_rate * 100, 2),
            "Avg PnL % per Trade": round(avg_pnl * 100, 2)
        })

        # === Equity vs Benchmark ===
        st.subheader("Equity Curve vs Benchmark")
        fig, ax = plt.subplots()
        ax.plot(df.index, df["Equity"], label=f"{ticker} Strategy")
        ax.plot(benchmark_equity.index, benchmark_equity.values, label="SPY Benchmark", linestyle="--")
        ax.legend()
        st.pyplot(fig)

        # === Drawdown ===
        st.subheader("Drawdown")
        drawdown = df["Equity"].cummax() - df["Equity"]
        fig, ax = plt.subplots()
        ax.plot(df.index, drawdown, color="red", label="Drawdown")
        ax.legend()
        st.pyplot(fig)

        # === Trade PnL Distribution ===
        st.subheader("Trade Return Distribution")
        fig, ax = plt.subplots()
        df["SignalReturn"].hist(bins=30, ax=ax)
        ax.set_title("Distribution of Trade Returns")
        st.pyplot(fig)

        # === Cumulative PnL ===
        st.subheader("Cumulative PnL")
        fig, ax = plt.subplots()
        df["SignalReturn"].cumsum().plot(ax=ax)
        st.pyplot(fig)

        # === Trade Log ===
        st.subheader("Trade Log")
        st.dataframe(trade_log)

    except Exception as e:
        st.error(e)
