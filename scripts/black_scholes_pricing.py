# -- Black-Scholes Pricing vs Market Price

# Import
import yfinance as yf
import pandas as pd
from datetime import datetime
import sys, os
sys.path.append(os.path.abspath("."))

from src.black_scholes import call_price, put_price

# Live SPY Price
print("Fetching live SPY price...")
data = yf.download("SPY", period="1d", progress=False)
S = float(data["Close"].squeeze())
print(f"Live SPY Price: ${S:.2f}")

# Load Option Data
df_call    = pd.read_csv("data/SPY_calls.csv")
df_put     = pd.read_csv("data/SPY_puts.csv")
EXPIRATION = df_call["expiration"].iloc[0]

# Find ATM options
call_option = df_call.iloc[(df_call["strike"] - S).abs().argmin()]
put_option  = df_put.iloc[(df_put["strike"] - S).abs().argmin()]

# Inputs
K      = call_option["strike"]
r      = 0.05
today  = datetime.today()
expiry = datetime.strptime(EXPIRATION, "%Y-%m-%d")
T      = max((expiry - today).days / 252, 1e-6)
sigma  = call_option["impliedVolatility"]

# Prices
bs_call  = round(call_price(S, K, T, r, sigma), 2)
bs_put   = round(put_price(S, K, T, r, sigma), 2)
mkt_call = round(call_option["lastPrice"], 2)
mkt_put  = round(put_option["lastPrice"], 2)

# Output
print(f"\n{'='*40}")
print(f"  Expiration : {EXPIRATION}")
print(f"  T (years)  : {T:.4f}")
print(f"  Strike (K) : ${K:.2f}")
print(f"  Sigma (IV) : {sigma:.4f}")
print(f"{'='*40}")
print(f"  {'':20} {'Call':>8} {'Put':>8}")
print(f"  {'Market Price':20} ${mkt_call:>7} ${mkt_put:>7}")
print(f"  {'Black-Scholes':20} ${bs_call:>7} ${bs_put:>7}")
print(f"  {'Difference':20} ${round(bs_call-mkt_call,2):>7} ${round(bs_put-mkt_put,2):>7}")
print(f"{'='*40}")