from src.sentiment_agent import SentimentAgent
from src.data_collector import DataCollectorAgent

class StrategyAgent:
    def __init__(self, tickers=["TSLA"]):
        self.tickers = tickers
        self.sentiment_agent = SentimentAgent()

    def analyze_news(self, ticker, top_n=5):
        collector = DataCollectorAgent(ticker)
        news_items = collector.get_news()[:top_n]
        scores = []
        for item in news_items:
            title = item["title"]
            sentiment = self.sentiment_agent.analyze(title)
            scores.append(sentiment)
        return scores

    def trading_signal(self, scores):
        avg_pos = sum(s["positive"] for s in scores) / len(scores)
        avg_neg = sum(s["negative"] for s in scores) / len(scores)

        if avg_pos > 0.6:
            return "Buy", avg_pos, avg_neg
        elif avg_neg > 0.6:
            return "Sell", avg_pos, avg_neg
        else:
            return "Hold", avg_pos, avg_neg

if __name__ == "__main__":
    agent = StrategyAgent(["TSLA", "AAPL", "NVDA"])
    for ticker in agent.tickers:
        scores = agent.analyze_news(ticker, top_n=5)
        signal, pos, neg = agent.trading_signal(scores)
        print(f"Ticker: {ticker}")
        print("  Trading Signal:", signal)
        print("  Avg Positive:", pos)
        print("  Avg Negative:", neg)
        print("-"*40)
