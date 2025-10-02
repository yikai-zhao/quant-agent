# Quant-Agent: Multi-Agent System for Quantitative Finance

## Overview
Quant-Agent is a modular pipeline for quantitative finance research. It integrates FinBERT for financial sentiment analysis and GPT-5 for reasoning and report generation. The system demonstrates model orchestration, prompt engineering, and deployment for real-world financial applications.

## Features
- Data collection from financial news, earnings calls, and market data
- Sentiment analysis using FinBERT
- Reasoning module with GPT-5 for event-driven market analysis
- Strategy generation with sentiment scores and technical indicators
- Report generation in Markdown or PDF
- Deployment with FastAPI and Docker

## Tech Stack
- Python, PyTorch, HuggingFace Transformers
- FinBERT, GPT-5 API
- FastAPI, Streamlit
- Docker, AWS or GCP

## Project Structure
quant-agent/
    src/
        data_collector.py
        sentiment_agent.py
        reasoning_agent.py
        strategy_agent.py
        report_agent.py
        orchestrator.py
    notebooks/
        demo_pipeline.ipynb
    examples/
        sample_report.md
        example_dashboard.png
    requirements.txt
    README.md
    Dockerfile

## Installation
git clone https://github.com/yikai-zhao/quant-agent.git
cd quant-agent
pip install -r requirements.txt

## Run Demo
python src/orchestrator.py

## License
MIT License

## Dashboard and Backtesting

Run the trading dashboard with:
\\\ash
streamlit run src/streamlit_app.py
\\\

Features:
- Real-time stock data via yfinance
- Technical indicators (RSI, SMA, MACD)
- Trading signals (MACD crossover strategy)
- Backtesting engine with equity curve and performance summary

## Key Features
- Multi-Agent architecture (data, sentiment, strategy, reporting)
- Real-time stock data via yfinance
- Technical indicators: RSI, SMA, MACD, Bollinger Bands, ATR
- Strategy signals (momentum, mean reversion, sentiment-driven)
- Backtesting with Sharpe Ratio, Max Drawdown, equity curve
- Streamlit Dashboard for visualization
- CI/CD with pytest

## Run Dashboard
\\\ash
streamlit run src/streamlit_app.py
\\\

## Example
![Dashboard Screenshot](example_dashboard.png)

## Key Features
- Multi-Agent architecture (data, sentiment, strategy, reporting)
- Real-time stock data via yfinance
- Technical indicators: RSI, SMA, MACD, Bollinger Bands, ATR
- Strategy signals (momentum, mean reversion, sentiment-driven)
- Backtesting with Sharpe Ratio, Max Drawdown, equity curve
- Streamlit Dashboard for visualization
- CI/CD with pytest

## Run Dashboard
\\\ash
streamlit run src/streamlit_app.py
\\\

## Example
![Dashboard Screenshot](example_dashboard.png)
