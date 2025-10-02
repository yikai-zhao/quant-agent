import numpy as np

class Backtester:
    def __init__(self, initial_balance=100000):
        self.balance = initial_balance
        self.positions = []
        self.history = []
        self.equity_curve = []

    def execute_signal(self, signal, price, size=1):
        if signal == "BUY":
            self.positions.append(price)
            self.history.append(("BUY", price))
        elif signal == "SELL" and self.positions:
            entry = self.positions.pop(0)
            pnl = (price - entry) * size
            self.balance += pnl
            self.history.append(("SELL", price, pnl))
        self.equity_curve.append(self.balance)

    def sharpe_ratio(self, returns, rf=0.0):
        excess = returns - rf
        return np.sqrt(252) * excess.mean() / excess.std()

    def max_drawdown(self):
        curve = np.array(self.equity_curve)
        peak = np.maximum.accumulate(curve)
        dd = (curve - peak) / peak
        return dd.min()

    def summary(self):
        returns = np.diff(self.equity_curve) / self.equity_curve[:-1] if len(self.equity_curve) > 1 else np.array([0])
        return {
            "final_balance": self.balance,
            "trades": len(self.history),
            "sharpe_ratio": float(self.sharpe_ratio(returns)) if len(returns) > 5 else None,
            "max_drawdown": float(self.max_drawdown()) if self.equity_curve else None
        }
