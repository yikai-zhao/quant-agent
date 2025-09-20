from src.signal_engine import SignalEngine
from src.data_collector import DataCollectorAgent
from src.sentiment_agent import SentimentAgent

class StrategyAgent:
    def __init__(self, ticker="TSLA"):
        self.ticker = ticker
        self.sentiment_agent = SentimentAgent()
        self.data_collector = DataCollectorAgent(ticker)
        self.signal_engine = SignalEngine()

    def analyze(self):
        # Collect sentiment
        news_items = self.data_collector.get_news()[:5]
        scores = []
        for item in news_items:
            sentiment = self.sentiment_agent.analyze(item["title"])
            scores.append(sentiment)
        avg_sentiment = sum(s["positive"] for s in scores) / len(scores) if scores else 0.5

        # Placeholder momentum (could be RSI, MA, etc.)
        stock_data = self.data_collector.get_stock_data(period="5d")
        momentum_score = 1 if stock_data["Close"].iloc[-1] > stock_data["Close"].mean() else 0.4

        # Placeholder fundamentals & macro (can be upgraded with APIs later)
        fundamental_score = 0.6
        macro_score = 0.5

        last_price = float(stock_data["Close"].iloc[-1])

        plan = self.signal_engine.generate_trade_plan(
            ticker=self.ticker,
            sentiment_score=avg_sentiment,
            momentum_score=momentum_score,
            fundamental_score=fundamental_score,
            macro_score=macro_score,
            price=last_price
        )

        return plan

if __name__ == "__main__":
    agent = StrategyAgent("TSLA")
    trade_plan = agent.analyze()
    print("Generated Trade Plan:")
    print(trade_plan)
