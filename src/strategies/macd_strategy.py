import numpy as np
from indicators import macd

def macd_strategy(prices):
    macd_line, signal_line = macd(prices)
    return np.where(macd_line > signal_line, 1, -1)
