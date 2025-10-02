import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from indicators import rsi, sma, macd, bollinger_bands
from backtester import Backtester

st.title("Quant-Agent Trading Dashboard")

# --- user input ---
tickers = st.text_input("Enter stock tickers (comma separated)", "AAPL,MSFT").split(",")
interval = st.selectbox("Select interval", ["1d", "1h", "15m"])
strategy = st.selectbox("Select strategy", ["MACD crossover", "SMA crossover", "RSI threshold", "Bollinger breakout"])

for ticker in [t.strip() for t in tickers]:
    st.header(f"Analysis for {ticker}")
    data = yf.download(ticker, period="6mo", interval=interval, auto_adjust=False)

    st.subheader("Price Chart")
    st.line_chart(data["Close"])

    bt = Backtester()

    signals = pd.DataFrame(index=data.index)
    signals["Price"] = data["Close"]

    if strategy == "MACD crossover":
        macd_line, signal_line = macd(data["Close"])
        signals["MACD"] = macd_line
        signals["Signal"] = signal_line
        signals["Position"] = np.where(signals["MACD"] > signals["Signal"], 1, -1)

    elif strategy == "SMA crossover":
        signals["SMA20"] = sma(data["Close"], 20)
        signals["SMA50"] = sma(data["Close"], 50)
        signals["Position"] = np.where(signals["SMA20"] > signals["SMA50"], 1, -1)

    elif strategy == "RSI threshold":
        signals["RSI"] = rsi(data["Close"])
        signals["Position"] = np.where(signals["RSI"] < 30, 1, np.where(signals["RSI"] > 70, -1, 0))

    elif strategy == "Bollinger breakout":
        upper, lower = bollinger_bands(data["Close"])
        signals["Upper"] = upper
        signals["Lower"] = lower
        signals["Position"] = np.where(data["Close"] < lower, 1, np.where(data["Close"] > upper, -1, 0))

    # backtest
    for i in range(1, len(signals)):
        if signals["Position"].iloc[i] == 1 and signals["Position"].iloc[i-1] <= 0:
            bt.execute_signal("BUY", signals["Price"].iloc[i])
        elif signals["Position"].iloc[i] == -1 and signals["Position"].iloc[i-1] >= 0:
            bt.execute_signal("SELL", signals["Price"].iloc[i])

    summary = bt.summary()
    st.subheader("Backtest Summary")
    st.json(summary)

    # equity curve
    if bt.equity_curve:
        equity_curve = pd.Series(bt.equity_curve, index=signals.index[:len(bt.equity_curve)])
        st.line_chart(pd.DataFrame({"Equity Curve": equity_curve}))

    # show buy/sell markers
    st.subheader("Trading Signals")
    buys = [i for i, h in enumerate(bt.history) if h[0] == "BUY"]
    sells = [i for i, h in enumerate(bt.history) if h[0] == "SELL"]
    st.write(f"Total Buys: {len(buys)}, Total Sells: {len(sells)}")
