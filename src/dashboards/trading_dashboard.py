import streamlit as st
import pandas as pd
import os
import datetime
import yfinance as yf
from src.strategy_agent import StrategyAgent
from src.trader_agent import TraderAgent

st.title("📈 Quant-Agent Trading Dashboard")

# Session state for trade plan
if "trade_plan" not in st.session_state:
    st.session_state.trade_plan = None

ticker = st.text_input("Enter ticker:", "TSLA")

if st.button("Generate Trade Plan"):
    agent = StrategyAgent(ticker)
    trade_plan = agent.analyze()
    st.session_state.trade_plan = trade_plan
    st.subheader("Generated Trade Plan")
    st.json(trade_plan)

if st.session_state.trade_plan:
    st.subheader("Generated Trade Plan")
    st.json(st.session_state.trade_plan)

    if st.button("Simulate Trade Execution"):
        trade_plan = st.session_state.trade_plan
        trader = TraderAgent()
        result = trader.execute_trade(trade_plan, qty=10)

        result["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result["confidence"] = trade_plan.get("confidence", 0)

        # Use real-time market price
        live_price = yf.Ticker(trade_plan["ticker"]).history(period="1d")["Close"].iloc[-1]
        entry_price = trade_plan.get("entry_price", live_price)
        stop_loss = trade_plan.get("stop_loss", entry_price * 0.95)
        take_profit = trade_plan.get("take_profit", entry_price * 1.05)

        # Compute PnL based on live price
        qty = 10
        if trade_plan.get("signal") == "BUY":
            pnl = (live_price - entry_price) * qty
        else:
            pnl = (entry_price - live_price) * qty

        result["entry_price"] = entry_price
        result["live_price"] = live_price
        result["pnl"] = pnl

        os.makedirs("results", exist_ok=True)
        file_path = "results/trade_history.csv"

        if os.path.exists(file_path):
            history = pd.read_csv(file_path)
        else:
            history = pd.DataFrame(columns=["timestamp","symbol","side","qty","status","confidence","entry_price","live_price","pnl"])

        history = pd.concat([history, pd.DataFrame([result])], ignore_index=True)
        history.to_csv(file_path, index=False)

        st.subheader("Trade History")
        st.dataframe(history)

        st.subheader("Cumulative PnL Curve")
        history["cumulative_pnl"] = history["pnl"].cumsum()
        st.line_chart(history[["cumulative_pnl"]])

        st.subheader("Confidence Distribution")
        st.bar_chart(history["confidence"])
