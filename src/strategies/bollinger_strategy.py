import numpy as np
from indicators import bollinger_bands

def bollinger_breakout(prices):
    upper, lower = bollinger_bands(prices)
    return np.where(prices < lower, 1, np.where(prices > upper, -1, 0))
