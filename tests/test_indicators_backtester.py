import pandas as pd
from src.indicators import rsi, sma, macd
from src.backtester import Backtester

def test_indicators():
    data = pd.Series(range(1,50))
    assert not rsi(data).isnull().all()
    assert not sma(data).isnull().all()
    macd_line, signal_line = macd(data)
    assert len(macd_line) == len(signal_line)

def test_backtester():
    bt = Backtester()
    bt.execute_signal("BUY", 100)
    bt.execute_signal("SELL", 110)
    s = bt.summary()
    assert s["final_balance"] >= 100000
