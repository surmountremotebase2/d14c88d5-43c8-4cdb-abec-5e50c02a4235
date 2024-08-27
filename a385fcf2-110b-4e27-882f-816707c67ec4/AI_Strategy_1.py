from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset
from surmount.technical_indicators import SMA, STDEV
from surmount.logging import log
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self):
        # A list of ticker symbols for SaaS companies we are interested in.
        self.tickers = ["CRM", "ADBE", "ZM", "WORK", "SHOP"]
        self.data_list = [Asset(i) for i in self.tickers]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        # Assuming a fixed risk-free rate
        risk_free_rate = 0.01
        
        # Dictionary to store Sharpe ratios for each asset
        sharpe_ratios = {}
        
        # Calculate return and volatility (as standard deviation) for each asset
        for ticker in self.tickers:
            # Assuming we can access data for the last 60 trading days
            prices = pd.Series([datum[ticker]["close"] for datum in data["ohlcv"][-60:]])
            
            # Daily returns
            returns = prices.pct_change().dropna()
            
            # Average daily return and daily standard deviation
            avg_daily_return = returns.mean()
            std_deviation = returns.std()
            
            # Sharpe ratio calculation
            sharpe_ratio = (avg_daily_return - risk_free_rate) / std_deviation
            sharpe_ratios[ticker] = sharpe_ratio
        
        # Normalize Sharpe ratios to get weights for allocation (ensure they sum to 1)
        total_sharpe = sum(sharpe_ratios.values())
        allocation_ratios = {ticker: ratio / total_sharpe for ticker, ratio in sharpe_ratios.items()}
        
        # Log for debugging
        log(f"Allocation Ratios based on Sharpe: {allocation_ratios}")
        
        return TargetAllocation(allocation_ratios)