# -- Historical Volatility Analysis

# Import
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys, os
sys.path.append(os.path.abspath("."))

from src.volatility import historical_volatility

# Fetch Data
print("Fetching SPY historical data...")
spy = yf.download("SPY", start="2020-10-01", end="2025-01-01", progress=False)

# Compute
returns     = np.log(spy["Close"] / spy["Close"].shift(1)).dropna()
vol = float(historical_volatility(spy["Close"]).squeeze())
rolling_vol = returns.squeeze().rolling(window=21).std() * np.sqrt(252)

print(f"Annualized Historical Volatility: {float(vol):.4f} ({float(vol)*100:.2f}%)")

# Helper for x-axis formatting
def format_xaxis(ax):
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

fig, axes = plt.subplots(3, 1, figsize=(14, 14))
fig.suptitle("SPY Historical Volatility Analysis (2020–2025)", fontsize=14)

# SPY Price
axes[0].plot(spy["Close"], color="blue")
axes[0].set_title("SPY Historical Prices")
axes[0].set_ylabel("Price ($)")
axes[0].grid(True)
format_xaxis(axes[0])

# Log Return Distribution
axes[1].hist(returns, bins=60, color="steelblue", edgecolor="white")
axes[1].set_title("SPY Log Return Distribution")
axes[1].set_xlabel("Log Return")
axes[1].set_ylabel("Frequency")
axes[1].grid(True)

# Rolling Volatility
axes[2].plot(rolling_vol, color="darkorange")
axes[2].axhline(float(vol), linestyle="--", color="red", alpha=0.7,
                label=f"Full-period vol: {float(vol)*100:.1f}%")
axes[2].set_title("21-Day Rolling Volatility")
axes[2].set_ylabel("Annualized Volatility")
axes[2].legend()
axes[2].grid(True)
format_xaxis(axes[2])

plt.tight_layout()
plt.savefig("outputs/historical_volatility.png", dpi=150)
plt.show()
print("Saved: outputs/historical_volatility.png")