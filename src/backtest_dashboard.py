import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from src.backtest_agent import BacktestAgent

st.title("📈 Quant-Agent Backtest Dashboard")

ticker = st.text_input("Enter ticker:", "TSLA")
start_date = st.date_input("Start date:", value=pd.to_datetime("2022-01-01"))
end_date = st.date_input("End date:", value=pd.to_datetime("2023-01-01"))

strategy_choice = st.selectbox(
    "Select Strategy:",
    ["Price Momentum", "Sentiment Driven", "Hybrid"]
)

if st.button("Run Backtest"):
    bt = BacktestAgent(ticker, start=str(start_date), end=str(end_date), initial_capital=10000)
    if strategy_choice == "Price Momentum":
        bt.mode = "momentum"
    elif strategy_choice == "Sentiment Driven":
        bt.mode = "sentiment"
    else:
        bt.mode = "hybrid"

    summary = bt.performance_summary()
    st.subheader("Performance Summary")
    st.write(summary)

    df = bt.run_backtest()
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(df.index, df["Equity"], label=f"{ticker} {strategy_choice}")
    ax.set_title(f"Equity Curve - {ticker} ({strategy_choice})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Equity ($)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
