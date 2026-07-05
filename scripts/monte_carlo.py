# -- Monte Carlo: Single Path, Multiple Paths, and BS Convergence

# Import
import numpy as np
import matplotlib.pyplot as plt
import sys, os
sys.path.append(os.path.abspath("."))

from src.monte_carlo import (
    simulate_stock_path,
    simulate_multiple_paths,
    monte_carlo_call_price,
    monte_carlo_put_price
)
from src.black_scholes import call_price, put_price

# Shared Parameters
S     = 100
K     = 100
T     = 1
r     = 0.05
sigma = 0.2
steps = 252

bs_call = call_price(S, K, T, r, sigma)
bs_put  = put_price(S, K, T, r, sigma)

# ── 1. Single Path ──────────────────────────────────────────────
path = simulate_stock_path(S, T, r, sigma, steps)

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(path, color="steelblue")
ax.axhline(K, linestyle="--", color="red", alpha=0.6, label=f"Strike (${K})")
ax.set_title("Simulated Stock Price Path (GBM)")
ax.set_xlabel("Trading Days")
ax.set_ylabel("Stock Price ($)")
ax.legend()
ax.grid(True)
plt.tight_layout()
plt.savefig("outputs/monte_carlo_single_path.png", dpi=150)
plt.show()
print("Saved: outputs/monte_carlo_single_path.png")

# ── 2. Multiple Paths ───────────────────────────────────────────
print("\nSimulating 100 paths...")
paths = simulate_multiple_paths(S, T, r, sigma, steps, num_simulations=100)

fig, ax = plt.subplots(figsize=(12, 6))
for path in paths:
    ax.plot(path, alpha=0.3, linewidth=0.8)
ax.axhline(K, linestyle="--", color="red", linewidth=1.5, label=f"Strike (${K})")
ax.set_title("Monte Carlo Simulated Stock Paths (100 Simulations)")
ax.set_xlabel("Trading Days")
ax.set_ylabel("Stock Price ($)")
ax.legend()
ax.grid(True)
plt.tight_layout()
plt.savefig("outputs/monte_carlo_multi_path.png", dpi=150)
plt.show()
print("Saved: outputs/monte_carlo_multi_path.png")

# ── 3. Convergence vs Black-Scholes ─────────────────────────────
print("\nRunning convergence analysis...")
simulation_counts = [10, 100, 500, 1000, 5000, 10000]
mc_calls = []
mc_puts  = []

for n in simulation_counts:
    np.random.seed(42)
    mc_calls.append(monte_carlo_call_price(S, K, T, r, sigma, steps, n))
    np.random.seed(42)
    mc_puts.append(monte_carlo_put_price(S, K, T, r, sigma, steps, n))
    print(f"  n={n:6d}  |  MC Call={mc_calls[-1]:.4f}  BS Call={bs_call:.4f}  |  MC Put={mc_puts[-1]:.4f}  BS Put={bs_put:.4f}")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Monte Carlo Convergence to Black-Scholes", fontsize=13)

axes[0].plot(simulation_counts, mc_calls, marker="o", label="MC Call Price", color="blue")
axes[0].axhline(bs_call, linestyle="--", color="red", label=f"BS Call (${bs_call:.2f})")
axes[0].set_title("Call Price Convergence")
axes[0].set_xlabel("Number of Simulations")
axes[0].set_ylabel("Option Price ($)")
axes[0].legend()
axes[0].grid(True)

axes[1].plot(simulation_counts, mc_puts, marker="o", label="MC Put Price", color="green")
axes[1].axhline(bs_put, linestyle="--", color="red", label=f"BS Put (${bs_put:.2f})")
axes[1].set_title("Put Price Convergence")
axes[1].set_xlabel("Number of Simulations")
axes[1].set_ylabel("Option Price ($)")
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.savefig("outputs/monte_carlo_convergence.png", dpi=150)
plt.show()
print("Saved: outputs/monte_carlo_convergence.png")