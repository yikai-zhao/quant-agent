import streamlit as st
import yfinance as yf
import pandas as pd
from indicators import rsi, sma, macd

st.title("Quant-Agent Trading Dashboard")

ticker = st.text_input("Enter stock ticker", "AAPL")

data = yf.download(ticker, period="6mo", interval="1d")

st.subheader(f"{ticker} Closing Prices (6M)")
st.line_chart(data["Close"])

st.subheader("Technical Indicators")
st.line_chart(rsi(data["Close"]))
st.line_chart(sma(data["Close"]))
macd_line, signal_line = macd(data["Close"])
st.line_chart(pd.DataFrame({"MACD": macd_line, "Signal": signal_line}))
