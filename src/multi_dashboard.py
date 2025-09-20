import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from src.data_collector import DataCollectorAgent
from src.sentiment_agent import SentimentAgent
from src.strategy_agent import StrategyAgent

st.title("📈 Quant-Agent Multi-Stock Sentiment Dashboard")

tickers = st.text_input("Enter tickers (comma separated):", "TSLA,AAPL,NVDA")
tickers = [t.strip().upper() for t in tickers.split(",")]

results = []

for ticker in tickers:
    st.subheader(f"📊 {ticker} Analysis")
    try:
        collector = DataCollectorAgent(ticker)
        stock_data = collector.get_stock_data(period="5d")
        news = collector.get_news()[:5]

        strat = StrategyAgent(ticker)
        scores = strat.analyze_news(ticker, top_n=5)
        signal, pos, neg = strat.trading_signal(scores)

        results.append({"Ticker": ticker, "Signal": signal, "Pos": pos, "Neg": neg})

        st.line_chart(stock_data["Close"])

        st.markdown(f"""
        **Trading Signal:** {signal}  
        **Avg Positive:** {pos:.3f}  
        **Avg Negative:** {neg:.3f}  
        """)

        st.markdown("**Latest News Headlines:**")
        for item in news:
            st.write(f"- [{item['title']}]({item['link']})")

    except Exception as e:
        st.error(f"Error processing {ticker}: {e}")

if results:
    st.subheader("📋 Summary of Signals")
    df = pd.DataFrame(results)
    st.dataframe(df)
