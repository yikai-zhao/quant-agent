import pandas as pd

class Backtester:
    def __init__(self, initial_balance=100000):
        self.balance = initial_balance
        self.positions = []
        self.history = []

    def execute_signal(self, signal, price, size=1):
        if signal == "BUY":
            self.positions.append(price)
            self.history.append(("BUY", price))
        elif signal == "SELL" and self.positions:
            entry = self.positions.pop(0)
            pnl = (price - entry) * size
            self.balance += pnl
            self.history.append(("SELL", price, pnl))

    def summary(self):
        return {
            "final_balance": self.balance,
            "trades": len(self.history),
            "open_positions": len(self.positions)
        }
