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
        if returns.std() == 0: return 0
        excess = returns - rf
        return np.sqrt(252) * excess.mean() / excess.std()

    def max_drawdown(self):
        if not self.equity_curve: return None
        curve = np.array(self.equity_curve)
        peak = np.maximum.accumulate(curve)
        dd = (curve - peak) / peak
        return dd.min()

    def calmar_ratio(self, returns):
        max_dd = abs(self.max_drawdown()) if self.max_drawdown() else 1
        if max_dd == 0: return None
        return returns.mean() * 252 / max_dd

    def win_rate(self):
        wins = [h for h in self.history if h[0] == "SELL" and h[2] > 0]
        trades = [h for h in self.history if h[0] == "SELL"]
        return len(wins) / len(trades) if trades else 0

    def summary(self):
        returns = np.diff(self.equity_curve) / self.equity_curve[:-1] if len(self.equity_curve) > 1 else np.array([0])
        return {
            "final_balance": self.balance,
            "trades": len(self.history),
            "sharpe_ratio": float(self.sharpe_ratio(returns)) if len(returns) > 5 else None,
            "max_drawdown": float(self.max_drawdown()) if self.equity_curve else None,
            "calmar_ratio": float(self.calmar_ratio(returns)) if len(returns) > 5 else None,
            "win_rate": float(self.win_rate())
        }
