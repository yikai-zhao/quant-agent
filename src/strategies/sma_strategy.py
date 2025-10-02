import numpy as np
from indicators import sma

def sma_crossover(prices):
    sma20 = sma(prices, 20)
    sma50 = sma(prices, 50)
    return np.where(sma20 > sma50, 1, -1)
