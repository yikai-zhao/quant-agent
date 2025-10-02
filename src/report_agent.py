import datetime

def generate_report(summary, ticker, strategy):
    report = f"""# Quant-Agent Report
**Date:** {datetime.date.today()}  
**Ticker:** {ticker}  
**Strategy:** {strategy}  

## Results
- Final Balance: {summary['final_balance']}
- Trades: {summary['trades']}
- Sharpe Ratio: {summary['sharpe_ratio']}
- Max Drawdown: {summary['max_drawdown']}
- Calmar Ratio: {summary['calmar_ratio']}
- Win Rate: {summary['win_rate']}

"""
    with open("report.md", "w") as f:
        f.write(report)
    return "report.md"
