# SPY Options Pricing & Volatility Analysis

A quantitative finance project that prices SPY options using Black-Scholes, computes the Greeks, estimates implied and historical volatility via Newton-Raphson, and simulates price paths with Monte Carlo methods.

---

## Project Structure

```
├── src/
│   ├── black_scholes.py      # Black-Scholes call/put pricing + d1/d2
│   ├── greeks.py             # Delta, Gamma, Vega, Theta, Rho
│   ├── volatility.py         # Historical volatility + IV solver (Newton-Raphson)
│   ├── monte_carlo.py        # GBM simulation + Monte Carlo option pricing
│   └── data_loader.py        # yfinance data download utilities
├── notebooks/
│   ├── black_scholes_pricing.ipynb   # Black-Scholes vs market price comparison
│   ├── greeks_visualization.ipynb    # Delta vs stock price plot
│   ├── implied_volatility.ipynb      # IV smile/curve from live SPY options chain
│   ├── monte_carlo_single.ipynb      # Single simulated GBM path
│   ├── monte_carlo_multi.ipynb       # 100 simulated paths
│   ├── monte_carlo_convergence.ipynb # MC vs BS convergence by simulation count
│   └── historical_volatility.ipynb   # Rolling vol, return distribution, SPY prices
├── data/
│   ├── SPY_prices.csv
│   ├── SPY_calls_expiration_2026-06-05.csv
│   └── SPY_puts_expiration_2026-06-05.csv
└── README.md
```

---

## Models & Methods

### Black-Scholes Pricing (`src/black_scholes.py`)

Prices European call and put options using the closed-form Black-Scholes formula:

$$C = S \cdot N(d_1) - K e^{-rT} \cdot N(d_2)$$
$$P = K e^{-rT} \cdot N(-d_2) - S \cdot N(-d_1)$$

Where:

$$d_1 = \frac{\ln(S/K) + (r + \frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}, \quad d_2 = d_1 - \sigma\sqrt{T}$$

**Assumptions:** European-style exercise, constant volatility and risk-free rate, no dividends, log-normally distributed returns.

---

### Greeks (`src/greeks.py`)

| Greek | Measures | Formula |
|-------|----------|---------|
| **Delta** | Sensitivity to stock price | $N(d_1)$ for calls, $N(d_1) - 1$ for puts |
| **Gamma** | Rate of change of Delta | $\frac{N'(d_1)}{S \sigma \sqrt{T}}$ |
| **Vega** | Sensitivity to volatility | $S \sqrt{T} \cdot N'(d_1)$ |
| **Theta** | Time decay (daily) | Annualized formula divided by 252 |
| **Rho** | Sensitivity to interest rate | $KTe^{-rT} \cdot N(d_2)$ for calls |

Theta is expressed as **daily decay** (divided by 252 trading days), which is the standard convention used by brokers and traders.

---

### Implied Volatility (`src/volatility.py`)

Uses **Newton-Raphson iteration** to back out the implied volatility $\sigma$ from a market option price:

$$\sigma_{n+1} = \sigma_n - \frac{f(\sigma_n)}{\text{Vega}(\sigma_n)}$$

Where $f(\sigma) = \text{BS\_Price}(\sigma) - \text{Market\_Price}$.

Converges when $|f(\sigma)| < 10^{-5}$, with a guard against near-zero vega (deep ITM/OTM options) that would cause division instability.

**Note on data quality:** Live bid/ask data from yfinance can be stale or corrupt for certain strikes. The IV notebook uses yfinance's pre-computed `impliedVolatility` field for the smile plot, while the Newton-Raphson solver is validated against synthetic clean prices.

---

### Historical Volatility (`src/volatility.py`)

Computed from realized log returns, annualized to 252 trading days:

$$\sigma_{hist} = \text{std}\left(\ln\frac{P_t}{P_{t-1}}\right) \times \sqrt{252}$$

The historical volatility notebook also plots a **21-day rolling volatility** window, showing how realized vol evolved across the 2020–2025 period (including the COVID spike and 2022 rate-hike volatility regime).

---

### Monte Carlo Simulation (`src/monte_carlo.py`)

Simulates stock price paths under **Geometric Brownian Motion (GBM)**:

$$S_{t+\Delta t} = S_t \cdot \exp\left[\left(r - \frac{1}{2}\sigma^2\right)\Delta t + \sigma\sqrt{\Delta t} \cdot Z\right], \quad Z \sim \mathcal{N}(0,1)$$

Option prices are estimated by averaging discounted payoffs across simulations:

$$C \approx e^{-rT} \cdot \frac{1}{N}\sum_{i=1}^{N} \max(S_T^{(i)} - K, 0)$$

The convergence notebook shows MC estimates vs the Black-Scholes closed-form price across simulation counts from 10 to 10,000, demonstrating that MC converges to BS as $N \to \infty$.

---

## Notebooks Overview

| Notebook | What It Shows |
|----------|--------------|
| `black_scholes_pricing` | Compares BS theoretical price to SPY market price for a real options contract |
| `greeks_visualization` | Plots call Delta as a function of stock price, illustrating nonlinear sensitivity |
| `implied_volatility` | Generates the IV smile/curve from the live SPY options chain |
| `historical_volatility` | SPY price history, log return distribution, and 21-day rolling volatility |
| `monte_carlo_single` | One simulated GBM path over 252 steps |
| `monte_carlo_multi` | 100 simultaneous GBM paths, showing dispersion of outcomes |
| `monte_carlo_convergence` | MC price convergence toward Black-Scholes as simulation count increases |

---

## Setup

**Requirements:** Python 3.9+

```bash
pip install numpy scipy pandas matplotlib yfinance
```

**Run any notebook:**
```bash
jupyter notebook notebooks/implied_volatility.ipynb
```

---

## Key Results

- **Monte Carlo converges to Black-Scholes** within ~1% by 5,000 simulations, validating the GBM implementation
- **IV smile is visible** across SPY strikes, with higher implied volatility on OTM puts (volatility skew), consistent with the market's demand for downside protection
- **21-day rolling volatility** shows clear volatility clustering: the COVID crash (March 2020), and the 2022 Fed tightening cycle both produced sustained elevated volatility regimes

---

## Limitations & Future Work

- **No dividends:** Black-Scholes as implemented assumes a non-dividend-paying asset. SPY pays a quarterly dividend; a more accurate model would use the continuous dividend yield adjustment: $d_1 = \frac{\ln(S/K) + (r - q + \frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}$
- **Constant volatility:** Black-Scholes assumes $\sigma$ is constant, but the IV smile itself proves it isn't. A natural extension would be a **local volatility** or **Heston stochastic volatility** model
- **American-style exercise:** SPY options are technically American-style. For puts especially, early exercise can matter; a binomial tree or Longstaff-Schwartz Monte Carlo would handle this correctly
- **Data source:** yfinance bid/ask data can be stale for certain strikes. A production system would use a paid data provider (CBOE DataShop, Tradier, Interactive Brokers)