import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from indicators import rsi, sma, macd
from backtester import Backtester

st.title("Quant-Agent Trading Dashboard")

# --- user input ---
ticker = st.text_input("Enter stock ticker", "AAPL")
data = yf.download(ticker, period="6mo", interval="1d")

# --- price chart ---
st.subheader(f"{ticker} Closing Prices (6M)")
st.line_chart(data["Close"])

# --- technical indicators ---
st.subheader("Technical Indicators")
st.line_chart(rsi(data["Close"]))
st.line_chart(sma(data["Close"]))
macd_line, signal_line = macd(data["Close"])
macd_df = pd.DataFrame({
    "MACD": macd_line.values,
    "Signal": signal_line.values
}, index=data.index)
st.line_chart(macd_df)

# --- generate trading signals based on MACD crossover ---
signals = pd.DataFrame(index=data.index)
signals["Price"] = data["Close"]
signals["MACD"] = macd_line
signals["Signal"] = signal_line
signals["Position"] = 0
signals.loc[signals["MACD"] > signals["Signal"], "Position"] = 1
signals.loc[signals["MACD"] < signals["Signal"], "Position"] = -1

# --- backtest ---
bt = Backtester()
for i in range(1, len(signals)):
    if signals["Position"].iloc[i] == 1 and signals["Position"].iloc[i-1] <= 0:
        bt.execute_signal("BUY", signals["Price"].iloc[i])
    elif signals["Position"].iloc[i] == -1 and signals["Position"].iloc[i-1] >= 0:
        bt.execute_signal("SELL", signals["Price"].iloc[i])

summary = bt.summary()

st.subheader("Backtest Results")
st.write(summary)

# equity curve
equity_curve = pd.Series([bt.balance for _ in range(len(signals))], index=signals.index)
st.line_chart(pd.DataFrame({"Equity Curve": equity_curve}))
