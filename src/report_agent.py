import datetime

def generate_report(summary, ticker, strategy):
    report = f"""# Quant-Agent Trading Report
**Date:** {datetime.date.today()}  
**Ticker:** {ticker}  
**Strategy:** {strategy}  

## Key Metrics
- Final Balance: {summary['final_balance']}
- Trades: {summary['trades']}
- Sharpe Ratio: {summary['sharpe_ratio']}
- Sortino Ratio: {summary['sortino_ratio']}
- Max Drawdown: {summary['max_drawdown']}
- Profit Factor: {summary['profit_factor']}
- CAGR: {summary['cagr']}

## Interpretation
This report provides a professional overview of trading strategy performance.  
It highlights risk-adjusted returns, downside risk, drawdowns, and profitability factors.  
"""

    path = f"report_{ticker}_{datetime.date.today()}.md"
    with open(path, "w") as f:
        f.write(report)
    return path
