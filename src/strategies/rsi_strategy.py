import numpy as np
from indicators import rsi

def rsi_strategy(prices):
    r = rsi(prices)
    return np.where(r < 30, 1, np.where(r > 70, -1, 0))
