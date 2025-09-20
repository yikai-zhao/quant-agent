import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from src.strategy_agent import StrategyAgent

class BacktestAgent:
    def __init__(self, ticker="TSLA", start="2022-01-01", end="2023-01-01", initial_capital=10000, mode="momentum"):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.initial_capital = initial_capital
        self.mode = mode
        self.data = yf.download(ticker, start=start, end=end)
        self.strategy_agent = StrategyAgent(ticker)

    def generate_signals(self):
        self.data["Return"] = self.data["Close"].pct_change()
        signal = 0

        if self.mode == "momentum":
            self.data["Signal"] = np.where(self.data["Return"] > 0, 1, -1)

        elif self.mode == "sentiment":
            try:
                scores = self.strategy_agent.analyze_news(top_n=5)
                avg_pos = np.mean([s["positive"] for s in scores])
                avg_neg = np.mean([s["negative"] for s in scores])
                if avg_pos > 0.6:
                    signal = 1
                elif avg_neg > 0.6:
                    signal = -1
                else:
                    signal = 0
            except Exception:
                signal = 0
            self.data["Signal"] = signal

        elif self.mode == "hybrid":
            momentum = np.where(self.data["Return"] > 0, 1, -1)
            try:
                scores = self.strategy_agent.analyze_news(top_n=5)
                avg_pos = np.mean([s["positive"] for s in scores])
                avg_neg = np.mean([s["negative"] for s in scores])
                if avg_pos > 0.6:
                    sentiment = 1
                elif avg_neg > 0.6:
                    sentiment = -1
                else:
                    sentiment = 0
            except Exception:
                sentiment = 0
            self.data["Signal"] = (momentum + sentiment) / 2

        return self.data

    def run_backtest(self):
        df = self.generate_signals()
        df["Strategy"] = df["Signal"].shift(1) * df["Return"]
        df["Equity"] = (1 + df["Strategy"]).cumprod() * self.initial_capital
        return df

    def performance_summary(self):
        df = self.run_backtest()
        total_return = float(df["Equity"].iloc[-1] / self.initial_capital - 1)
        sharpe_ratio = float(np.mean(df["Strategy"]) / np.std(df["Strategy"]) * np.sqrt(252))
        return {
            "Ticker": self.ticker,
            "Strategy": self.mode,
            "Total Return": total_return,
            "Sharpe Ratio": sharpe_ratio
        }

    def plot_equity_curve(self):
        df = self.run_backtest()
        plt.figure(figsize=(10,6))
        plt.plot(df.index, df["Equity"], label=f"{self.ticker} {self.mode}")
        plt.title(f"Equity Curve - {self.ticker} ({self.mode})")
        plt.xlabel("Date")
        plt.ylabel("Equity ($)")
        plt.legend()
        plt.grid(True)
        os.makedirs("results", exist_ok=True)
        file_path = f"results/{self.ticker}_{self.mode}_equity_curve.png"
        plt.savefig(file_path)
        print(f"Equity curve saved to {file_path}")

if __name__ == "__main__":
    bt = BacktestAgent("TSLA", start="2022-01-01", end="2023-01-01", mode="hybrid")
    summary = bt.performance_summary()
    print("Backtest Summary:")
    print(summary)
    bt.plot_equity_curve()
