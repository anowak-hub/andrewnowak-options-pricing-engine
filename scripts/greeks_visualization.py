# -- Greeks Visualization (Delta, Gamma, Theta, Vega vs Stock Price)

# Import
import numpy as np
import matplotlib.pyplot as plt
import sys, os
sys.path.append(os.path.abspath("."))

from src.greeks import call_delta, put_delta, gamma, call_theta, put_theta, vega

# Parameters
K     = 100
T     = 1
r     = 0.05
sigma = 0.2
stock_prices = np.linspace(50, 150, 300)

# Compute Greeks
call_deltas = [call_delta(S, K, T, r, sigma) for S in stock_prices]
put_deltas  = [put_delta(S, K, T, r, sigma)  for S in stock_prices]
gammas      = [gamma(S, K, T, r, sigma)       for S in stock_prices]
call_thetas = [call_theta(S, K, T, r, sigma)  for S in stock_prices]
put_thetas  = [put_theta(S, K, T, r, sigma)   for S in stock_prices]
vegas       = [vega(S, K, T, r, sigma)         for S in stock_prices]

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Option Greeks vs Stock Price (K=100, T=1yr, σ=0.2, r=0.05)", fontsize=14)

# Delta
axes[0, 0].plot(stock_prices, call_deltas, label="Call Delta", color="blue")
axes[0, 0].plot(stock_prices, put_deltas,  label="Put Delta",  color="red")
axes[0, 0].axvline(K, linestyle="--", color="gray", alpha=0.5, label="Strike")
axes[0, 0].set_title("Delta")
axes[0, 0].set_xlabel("Stock Price")
axes[0, 0].set_ylabel("Delta")
axes[0, 0].legend()
axes[0, 0].grid(True)

# Gamma
axes[0, 1].plot(stock_prices, gammas, color="green")
axes[0, 1].axvline(K, linestyle="--", color="gray", alpha=0.5, label="Strike")
axes[0, 1].set_title("Gamma (Call = Put)")
axes[0, 1].set_xlabel("Stock Price")
axes[0, 1].set_ylabel("Gamma")
axes[0, 1].legend()
axes[0, 1].grid(True)

# Theta
axes[1, 0].plot(stock_prices, call_thetas, label="Call Theta", color="blue")
axes[1, 0].plot(stock_prices, put_thetas,  label="Put Theta",  color="red")
axes[1, 0].axvline(K, linestyle="--", color="gray", alpha=0.5, label="Strike")
axes[1, 0].set_title("Theta (Daily Decay)")
axes[1, 0].set_xlabel("Stock Price")
axes[1, 0].set_ylabel("Theta")
axes[1, 0].legend()
axes[1, 0].grid(True)

# Vega
axes[1, 1].plot(stock_prices, vegas, color="purple")
axes[1, 1].axvline(K, linestyle="--", color="gray", alpha=0.5, label="Strike")
axes[1, 1].set_title("Vega (Call = Put)")
axes[1, 1].set_xlabel("Stock Price")
axes[1, 1].set_ylabel("Vega")
axes[1, 1].legend()
axes[1, 1].grid(True)

plt.tight_layout()
plt.savefig("outputs/greeks_visualization.png", dpi=150)
plt.show()
print("Saved: outputs/greeks_visualization.png")