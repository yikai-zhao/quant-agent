class RiskAgent:
    def __init__(self, max_position=0.1, stop_loss=0.05, take_profit=0.1):
        self.max_position = max_position
        self.stop_loss = stop_loss
        self.take_profit = take_profit

    def check_risk(self, portfolio_value, position_size, entry_price, current_price):
        if position_size > portfolio_value * self.max_position:
            return False, "Position size exceeds risk limit"
        if (current_price - entry_price) / entry_price <= -self.stop_loss:
            return False, "Stop loss triggered"
        if (current_price - entry_price) / entry_price >= self.take_profit:
            return False, "Take profit triggered"
        return True, "Within risk limits"
