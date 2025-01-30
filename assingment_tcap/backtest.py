import os
import pandas as pd


class BollingerBandStrategy:
    def __init__(self, data, token):
        self.data = data
        self.token = token
        self.trades = []

    def calculate_bollinger_bands(self, window=20):
        self.data['MA'] = self.data['Close'].rolling(window=window).mean()
        self.data['STD'] = self.data['Close'].rolling(window=window).std()
        self.data['Upper Band'] = self.data['MA'] + (2 * self.data['STD'])
        self.data['Lower Band'] = self.data['MA'] - (2 * self.data['STD'])

    def backtest(self):
        self.calculate_bollinger_bands()
        in_trade = False
        entry_price = 0
        entry_date = None

        for i, row in self.data.iterrows():
            # Buy 
            if not in_trade and row['Close'] < row['Lower Band'] * 0.97:
                in_trade = True
                entry_price = row['Close']
                entry_date = row.name
            # Sell 
            elif in_trade and row['Close'] >= row['Upper Band']:
                in_trade = False
                exit_price = row['Close']
                exit_date = row.name
                profit = (exit_price - entry_price) / entry_price * 100
                self.trades.append({
                    "token": self.token,
                    "date_in": entry_date,
                    "buy_price": entry_price,
                    "date_out": exit_date,
                    "sell_price": exit_price,
                    "profit_percentage": profit
                })

        if in_trade:
            exit_price = self.data.iloc[-1]['Close']
            exit_date = self.data.index[-1]
            profit = (exit_price - entry_price) / entry_price * 100
            self.trades.append({
                "token": self.token,
                "date_in": entry_date,
                "buy_price": entry_price,
                "date_out": exit_date,
                "sell_price": exit_price,
                "profit_percentage": profit
            })

        return pd.DataFrame(self.trades)


data_folder = "market_data"
result_file = "backtest_results.csv"
all_trades = []

for file in os.listdir(data_folder):
    if file.endswith(".csv"):
        token = file.split(".")[0]
        data = pd.read_csv(os.path.join(data_folder, file), parse_dates=["Date"], index_col="Date")
        strategy = BollingerBandStrategy(data, token)
        trades = strategy.backtest()
        all_trades.append(trades)

final_trades = pd.concat(all_trades, ignore_index=True)
final_trades.to_csv(result_file, index=False)
print(f"Backtest complete. Results saved to {result_file}.")
