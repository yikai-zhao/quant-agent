import streamlit as st
import pandas as pd
import os
import datetime
import plotly.graph_objects as go
from src.strategy_agent import StrategyAgent
from src.trader_agent import TraderAgent
from src.signal_engine import SignalEngine

st.title("Quant-Agent Trading Dashboard")

ticker = st.text_input("Enter ticker:", "TSLA")

if st.button("Generate Trade Plan"):
    agent = StrategyAgent(ticker)
    trade_plan = agent.analyze()
    st.subheader("Generated Trade Plan")
    st.json(trade_plan)

    # Plot price and SMA
    engine = SignalEngine("config/strategy.yaml")
    data = engine.compute_indicators(ticker)

    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data["Open"],
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        name="Price"
    ))
    fig.add_trace(go.Scatter(x=data.index, y=data["SMA20"], mode="lines", name="SMA20"))
    fig.add_trace(go.Scatter(x=data.index, y=data["SMA50"], mode="lines", name="SMA50"))
    st.plotly_chart(fig, use_container_width=True)

    # RSI chart
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=data.index, y=data["RSI"], mode="lines", name="RSI"))
    fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
    fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
    st.subheader("RSI Indicator")
    st.plotly_chart(fig_rsi, use_container_width=True)

    # MACD chart
    fig_macd = go.Figure()
    fig_macd.add_trace(go.Scatter(x=data.index, y=data["MACD"], mode="lines", name="MACD"))
    fig_macd.add_trace(go.Scatter(x=data.index, y=data["Signal"], mode="lines", name="Signal"))
    st.subheader("MACD Indicator")
    st.plotly_chart(fig_macd, use_container_width=True)

    if st.button("Simulate Trade Execution"):
        trader = TraderAgent()
        result = trader.execute_trade(trade_plan, qty=10)
        result["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result["confidence"] = trade_plan.get("confidence", 0)

        os.makedirs("results", exist_ok=True)
        file_path = "results/trade_history.csv"

        if os.path.exists(file_path):
            history = pd.read_csv(file_path)
        else:
            history = pd.DataFrame(columns=["timestamp","symbol","side","qty","status","confidence"])

        history = pd.concat([history, pd.DataFrame([result])], ignore_index=True)
        history.to_csv(file_path, index=False)

        st.subheader("Trade History")
        st.dataframe(history)

        st.subheader("Confidence Distribution")
        st.bar_chart(history["confidence"])
