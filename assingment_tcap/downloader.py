import os
import yfinance as yf

# List of 50 stocks
assets = [
    "BTC-USD", "ETH-USD", "ADA-USD", "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA",
    "META", "NVDA", "JPM", "V", "JNJ", "WMT", "PG", "MA", "HD", "UNH", "DIS",
    "BAC", "KO", "PFE", "CSCO", "PEP", "XOM", "NFLX", "INTC", "CVX", "ADBE",
    "MRK", "T", "NKE", "CMCSA", "ORCL", "ABBV", "ACN", "CRM", "COST", "MDT",
    "AVGO", "QCOM", "TXN", "TMO", "IBM", "LIN", "AMGN", "PM", "PYPL", "SBUX"
]

output_folder = "market_data"
os.makedirs(output_folder, exist_ok=True)

for asset in assets:
    print(f"Downloading {asset} data...")
    data = yf.download(asset, interval="1d", period="1y")
    file_path = os.path.join(output_folder, f"{asset}.csv")
    data.to_csv(file_path)
    print(f"{asset} data saved to {file_path}")

print("All data downloaded.")
