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
expiration = spy.options[4]

options_chain = spy.option_chain(expiration)
calls = options_chain.calls
calls["expiration"] = expiration
save_data(calls, "SPY_calls.csv")

puts = options_chain.puts
puts["expiration"]  = expiration
save_data(puts, "SPY_puts.csv")