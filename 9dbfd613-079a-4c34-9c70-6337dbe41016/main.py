from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.data import Asset
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self):
        # Define a list of pharma and technology firms.
        # Update this list based on the firms you're interested in.
        self.tickers = ["PFE", "MRNA", "AAPL", "MSFT"]
        self.data_list = [Asset(i) for i in self.tickers]

    @property
    def interval(self):
        # Set the interval for data retrieval, "1day" for daily analysis.
        return "1day"

    @property
    def assets(self):
        # Return the list of tickers we're interested in.
        return self.tickers

    @property
    def data(self):
        # Define the list of data sources required for the strategy.
        return self.data_list

    def run(self, data):
        # This strategy will rank assets based on their recent price change
        # as a simple measure to indicate momentum and proxy for return expectation.
        price_changes = {}
        for ticker in self.tickers:
            # Check if we have enough data for analysis.
            if len(data["ohlcv"]) > 1:
                # Calculate the price change.
                closing_prices = [d[ticker]['close'] for d in data["ohlcv"]][-2:]  # Get the last two closing prices.
                price_change = (closing_prices[-1] - closing_prices[-2]) / closing_prices[-2]
                price_changes[ticker] = price_change
        
        # Normalize price changes to get allocations (this is a simple proxy approach and may need adjustments).
        total_change = sum(abs(value) for value in price_changes.values())
        
        # Avoid division by zero if total_change is zero.
        if total_change == 0:
            allocation_dict = {ticker: 1/len(self.tickers) for ticker in self.tickers}
        else:
            allocation_dict = {ticker: abs(change) / total_change for ticker, change in price_changes.items()}
        
        # Return TargetAllocation with allocations based on normalized price changes.
        return TargetAllocation(allocation_dict)