import datetime

def generate_report(summary, ticker, strategy):
    report = f"""# Quant-Agent Trading Report
**Date:** {datetime.date.today()}  
**Ticker:** {ticker}  
**Strategy:** {strategy}  

## Performance Metrics
- Final Balance: {summary['final_balance']}
- Trades: {summary['trades']}
- Sharpe Ratio: {summary['sharpe_ratio']}
- Max Drawdown: {summary['max_drawdown']}
- Calmar Ratio: {summary['calmar_ratio']}
- Win Rate: {summary['win_rate']}

## Interpretation
The selected strategy was applied to {ticker}.  
The Sharpe ratio reflects the risk-adjusted return.  
The maximum drawdown indicates the worst historical decline.  
The Calmar ratio compares annualized return to risk.  
Win rate shows the proportion of profitable trades.  

This report provides a quantitative overview, not investment advice.  
"""
    path = f"report_{ticker}_{datetime.date.today()}.md"
    with open(path, "w") as f:
        f.write(report)
    return path
