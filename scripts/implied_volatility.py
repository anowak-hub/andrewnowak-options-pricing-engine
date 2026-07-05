# -- IV Smile Curve From SPY Options Chain

# Import
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import sys, os
sys.path.append(os.path.abspath("."))

# Fetch Live Data
print("Fetching SPY options chain...")
ticker     = yf.Ticker("SPY")
expiration = ticker.options[6]
chain      = ticker.option_chain(expiration)
calls      = chain.calls
puts       = chain.puts

data = yf.download("SPY", period="1d", progress=False)
S    = float(data["Close"].squeeze())

today  = datetime.today()
expiry = datetime.strptime(expiration, "%Y-%m-%d")
T      = max((expiry - today).days / 252, 1e-6)

print(f"SPY Price : ${S:.2f}")
print(f"Expiration: {expiration}  (T={T:.4f})")

# Build IV Curve
def extract_iv_curve(chain_df):
    strikes, ivs = [], []
    for _, opt in chain_df.iterrows():
        try:
            K  = float(opt["strike"])
            iv = float(opt["impliedVolatility"])
            if np.isnan(iv) or iv <= 0:
                continue
            strikes.append(K)
            ivs.append(iv)
        except Exception:
            continue
    return pd.DataFrame({"strike": strikes, "iv": ivs}).sort_values("strike")

df_calls = extract_iv_curve(calls)
df_puts  = extract_iv_curve(puts)

print(f"Valid call strikes: {len(df_calls)}")
print(f"Valid put strikes:  {len(df_puts)}")

# Plot
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle(f"SPY Implied Volatility Smile  |  Exp: {expiration}  |  S=${S:.2f}", fontsize=13)

axes[0].plot(df_calls["strike"], df_calls["iv"], color="blue")
axes[0].axvline(S, linestyle="--", color="gray", alpha=0.6, label=f"Spot (${S:.0f})")
axes[0].set_title("Calls")
axes[0].set_xlabel("Strike Price")
axes[0].set_ylabel("Implied Volatility")
axes[0].legend()
axes[0].grid(True)

axes[1].plot(df_puts["strike"], df_puts["iv"], color="red")
axes[1].axvline(S, linestyle="--", color="gray", alpha=0.6, label=f"Spot (${S:.0f})")
axes[1].set_title("Puts")
axes[1].set_xlabel("Strike Price")
axes[1].set_ylabel("Implied Volatility")
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.savefig("outputs/implied_volatility_smile.png", dpi=150)
plt.show()
print("Saved: outputs/implied_volatility_smile.png")