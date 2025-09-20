import streamlit as st
import matplotlib.pyplot as plt
from src.sentiment_agent import SentimentAgent

st.title("Quant-Agent Sentiment Dashboard")
st.write("Enter financial news or statements below:")

user_input = st.text_area("Input Text", "Tesla announced record profits this quarter.")

if st.button("Analyze"):
    agent = SentimentAgent()
    result = agent.analyze(user_input)
    st.subheader("Sentiment Scores")
    st.write(result)

    # Trading Signal
    signal = "Hold"
    if result["positive"] 
        signal = "Buy"
    elif result["negative"] 
        signal = "Sell"
    st.subheader("Trading Signal")
    st.write(signal)

    # Plot sentiment chart
    labels = list(result.keys())
    values = list(result.values())
    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_ylabel("Score")
    ax.set_title("Sentiment Analysis")
    st.pyplot(fig)
