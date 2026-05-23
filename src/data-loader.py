# -- Where we generate data utilizing the yfinance library

# Library Import
import yfinance as yf
import pandas as pd 

# Download Historical stock price data
def download_stock_data(ticker: str, period="1y"):
    df = yf.download(ticker, period=period)
    return df

def save_data(df, filename):
    df.to_csv(f"data/{filename}")


df = download_stock_data("SPY")
save_data(df, "SPY_prices.csv")

# Download options chain data for a specified expiration date
spy = yf.Ticker("SPY")

expiration = "2026-06-05"
options_chain = spy.option_chain(expiration)
calls = options_chain.calls
save_data(calls, "SPY_calls_expiration_2026-06-05.csv")

puts = options_chain.puts
save_data(puts, "SPY_puts_expiration_2026-06-05.csv")