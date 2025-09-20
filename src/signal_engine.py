import yfinance as yf
import pandas as pd

class SignalEngine:
    def __init__(self, lookback=30):
        self.lookback = lookback

    def compute_indicators(self, ticker):
        data = yf.download(ticker, period='6mo', interval='1d')
        data['SMA20'] = data['Close'].rolling(window=20).mean()
        data['SMA50'] = data['Close'].rolling(window=50).mean()

        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))

        exp1 = data['Close'].ewm(span=12, adjust=False).mean()
        exp2 = data['Close'].ewm(span=26, adjust=False).mean()
        data['MACD'] = exp1 - exp2
        data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
        return data.dropna()

    def generate_trade_plan(self, ticker, sentiment_score, momentum_score, fundamental_score, macro_score, price):
        data = self.compute_indicators(ticker)
        latest = data.iloc[-1]

        sma20 = float(latest['SMA20'])
        sma50 = float(latest['SMA50'])
        rsi = float(latest['RSI'])
        macd = float(latest['MACD'])
        sig = float(latest['Signal'])

        score = (
            0.3 * sentiment_score +
            0.2 * momentum_score +
            0.2 * fundamental_score +
            0.1 * macro_score
        )

        if sma20 > sma50:
            score += 0.1
        if macd > sig:
            score += 0.1
        if rsi < 30:
            score += 0.05
        elif rsi > 70:
            score -= 0.05

        signal = 'BUY' if score > 0.55 else 'SELL' if score < 0.45 else 'HOLD'

        return {
            'ticker': ticker,
            'signal': signal,
            'confidence': round(score, 3),
            'entry_price': price,
            'stop_loss': round(price * 0.95, 2),
            'take_profit': round(price * 1.1, 2),
            'indicators': {
                'SMA20': round(sma20, 2),
                'SMA50': round(sma50, 2),
                'RSI': round(rsi, 2),
                'MACD': round(macd, 2),
                'Signal': round(sig, 2)
            },
            'rationale': {
                'sentiment_score': sentiment_score,
                'momentum_score': momentum_score,
                'fundamental_score': fundamental_score,
                'macro_score': macro_score
            }
        }
