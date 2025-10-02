import streamlit as st
import yfinance as yf
import pandas as pd
from backtester import Backtester
from strategies.macd_strategy import macd_strategy
from strategies.sma_strategy import sma_crossover
from strategies.rsi_strategy import rsi_strategy
from strategies.bollinger_strategy import bollinger_breakout

st.set_page_config(page_title="Quant-Agent Dashboard", layout="wide")
st.title("Quant-Agent Trading Dashboard")

tickers = st.text_input("Enter stock tickers (comma separated)", "AAPL,MSFT").split(",")
interval = st.selectbox("Select interval", ["1d", "1h", "15m"])
strategy = st.selectbox("Select strategy", ["MACD", "SMA", "RSI", "Bollinger"])

for ticker in [t.strip() for t in tickers]:
    st.header(f"Analysis for {ticker}")
    data = yf.download(ticker, period="6mo", interval=interval, auto_adjust=False)

    # select strategy
    if strategy == "MACD":
        positions = macd_strategy(data["Close"])
    elif strategy == "SMA":
        positions = sma_crossover(data["Close"])
    elif strategy == "RSI":
        positions = rsi_strategy(data["Close"])
    else:
        positions = bollinger_breakout(data["Close"])

    # run backtest
    bt = Backtester()
    for i in range(1, len(positions)):
        if positions[i] == 1 and positions[i-1] <= 0:
            bt.execute_signal("BUY", data["Close"].iloc[i])
        elif positions[i] == -1 and positions[i-1] >= 0:
            bt.execute_signal("SELL", data["Close"].iloc[i])

    summary = bt.summary()

    # KPI Cards
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Final Balance", f"")
    col2.metric("Sharpe Ratio", f"{summary['sharpe_ratio']:.2f}" if summary['sharpe_ratio'] else "N/A")
    col3.metric("Sortino Ratio", f"{summary['sortino_ratio']:.2f}" if summary['sortino_ratio'] else "N/A")
    col4.metric("Max Drawdown", f"{summary['max_drawdown']:.2%}" if summary['max_drawdown'] else "N/A")
    col5.metric("Profit Factor", f"{summary['profit_factor']:.2f}" if summary['profit_factor'] else "N/A")
    col6.metric("CAGR", f"{summary['cagr']:.2%}" if summary['cagr'] else "N/A")

    # Charts
    st.subheader("Equity Curve")
    if bt.equity_curve:
        st.line_chart(pd.Series(bt.equity_curve, index=data.index[:len(bt.equity_curve)]))

    # Mark buy/sell points on price chart
    st.subheader("Price with Trade Signals")
    trade_df = data.copy()
    trade_df["Position"] = positions
    st.line_chart(trade_df[["Close"]])
