import yfinance as yf
from yahoo_fin import news

class DataCollectorAgent:
    def __init__(self, ticker="TSLA"):
        self.ticker = ticker

    def get_stock_data(self, period="5d", interval="1d"):
        stock = yf.Ticker(self.ticker)
        hist = stock.history(period=period, interval=interval)
        return hist

    def get_news(self):
        headlines = news.get_yf_rss(self.ticker)
        return headlines

if __name__ == "__main__":
    agent = DataCollectorAgent("TSLA")
    print("=== Stock Data ===")
    print(agent.get_stock_data().tail())
    print("\n=== News Headlines ===")
    print(agent.get_news()[:5])
