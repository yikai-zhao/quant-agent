from src.signal_engine import SignalEngine

engine = SignalEngine("config/strategy.yaml")
plan = engine.generate_trade_plan(
    ticker="TSLA",
    sentiment_score=0.7,
    momentum_score=0.6,
    fundamental_score=0.55,
    macro_score=0.5,
    price=420.0
)
print(plan)
