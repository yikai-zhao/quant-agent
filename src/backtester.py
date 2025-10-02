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

    def sharpe_ratio(self, returns):
        return np.sqrt(252) * returns.mean() / returns.std() if returns.std() else None

    def sortino_ratio(self, returns):
        downside = returns[returns < 0]
        return np.sqrt(252) * returns.mean() / downside.std() if downside.std() else None

    def max_drawdown(self):
        if not self.equity_curve: return None
        curve = np.array(self.equity_curve)
        peak = np.maximum.accumulate(curve)
        dd = (curve - peak) / peak
        return dd.min()

    def profit_factor(self):
        gains = sum([h[2] for h in self.history if h[0] == "SELL" and h[2] > 0])
        losses = abs(sum([h[2] for h in self.history if h[0] == "SELL" and h[2] < 0]))
        return gains / losses if losses > 0 else None

    def cagr(self, years=0.5):
        if not self.equity_curve: return None
        final = self.equity_curve[-1]
        return (final / self.equity_curve[0]) ** (1/years) - 1 if years else None

    def summary(self):
        returns = np.diff(self.equity_curve) / self.equity_curve[:-1] if len(self.equity_curve) > 1 else np.array([0])
        return {
            "final_balance": self.balance,
            "trades": len(self.history),
            "sharpe_ratio": float(self.sharpe_ratio(returns)) if len(returns) > 5 else None,
            "sortino_ratio": float(self.sortino_ratio(returns)) if len(returns) > 5 else None,
            "max_drawdown": float(self.max_drawdown()) if self.equity_curve else None,
            "profit_factor": float(self.profit_factor()) if self.history else None,
            "cagr": float(self.cagr()) if self.equity_curve else None
        }
