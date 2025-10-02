import streamlit as st
import pandas as pd
from indicators import rsi, sma, macd

st.title("Quant-Agent Trading Dashboard")

data = pd.read_csv("examples/demo_prices.csv")
st.line_chart(data["Close"])

st.subheader("Indicators")
st.line_chart(rsi(data["Close"]))
st.line_chart(sma(data["Close"]))
macd_line, signal_line = macd(data["Close"])
st.line_chart(pd.DataFrame({"MACD": macd_line, "Signal": signal_line}))
