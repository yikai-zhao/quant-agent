import os
from src.strategy_agent import StrategyAgent

try:
    import alpaca_trade_api as tradeapi
except ImportError:
    tradeapi = None

class TraderAgent:
    def __init__(self, api_key=None, api_secret=None, base_url="https://paper-api.alpaca.markets"):
        self.api_key = api_key or os.getenv("ALPACA_API_KEY")
        self.api_secret = api_secret or os.getenv("ALPACA_API_SECRET")
        self.base_url = base_url
        if tradeapi and self.api_key and self.api_secret:
            self.api = tradeapi.REST(self.api_key, self.api_secret, base_url=self.base_url)
        else:
            self.api = None

    def execute_trade(self, plan, qty=1):
        if not self.api:
            print("No API configured. Simulating trade...")
            return {
                "symbol": plan["ticker"],
                "side": plan["signal"].lower(),
                "qty": qty,
                "status": "simulated"
            }
        if plan["signal"] == "BUY":
            side = "buy"
        elif plan["signal"] == "SELL":
            side = "sell"
        else:
            return {"symbol": plan["ticker"], "side": "hold", "qty": 0, "status": "no trade"}
        order = self.api.submit_order(
            symbol=plan["ticker"],
            qty=qty,
            side=side,
            type="market",
            time_in_force="gtc"
        )
        return order._raw

if __name__ == "__main__":
    agent = StrategyAgent("TSLA")
    plan = agent.analyze()
    print("Generated Trade Plan:", plan)

    trader = TraderAgent()  # no API keys, runs in simulation mode
    result = trader.execute_trade(plan, qty=10)
    print("Trade Result:", result)
