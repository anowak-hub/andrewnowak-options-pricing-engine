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
├── scripts/
│   ├── black_scholes_pricing.py   # BS vs market price comparison
│   ├── greeks_visualization.py    # Delta, Gamma, Theta, Vega plots
│   ├── implied_volatility.py      # IV smile/curve from live SPY options chain
│   ├── historical_volatility.py   # Rolling vol, return distribution, SPY prices
│   └── monte_carlo.py             # Single path, multiple paths, BS convergence
├── tests/
│   ├── test_black_scholes.py
│   ├── test_greeks.py
│   ├── test_monte_carlo.py
│   └── test_volatility.py
├── outputs/                       # Generated plots (auto-saved on script run)
├── data/
│   ├── SPY_prices.csv
│   ├── SPY_calls.csv
│   └── SPY_puts.csv
├── requirements.txt
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

**Note on data quality:** Live bid/ask data from yfinance can be stale or corrupt for certain strikes. The IV script uses yfinance's pre-computed `impliedVolatility` field for the smile plot, while the Newton-Raphson solver is validated against synthetic clean prices.

---

### Historical Volatility (`src/volatility.py`)

Computed from realized log returns, annualized to 252 trading days:

$$\sigma_{hist} = \text{std}\left(\ln\frac{P_t}{P_{t-1}}\right) \times \sqrt{252}$$

The historical volatility script plots a **21-day rolling volatility** window, showing how realized vol evolved across the 2020–2025 period (including the COVID crash and 2022 rate-hike volatility regime).

---

### Monte Carlo Simulation (`src/monte_carlo.py`)

Simulates stock price paths under **Geometric Brownian Motion (GBM)**:

$$S_{t+\Delta t} = S_t \cdot \exp\left[\left(r - \frac{1}{2}\sigma^2\right)\Delta t + \sigma\sqrt{\Delta t} \cdot Z\right], \quad Z \sim \mathcal{N}(0,1)$$

Option prices are estimated by averaging discounted payoffs across simulations:

$$C \approx e^{-rT} \cdot \frac{1}{N}\sum_{i=1}^{N} \max(S_T^{(i)} - K, 0)$$

The convergence script shows MC estimates vs the Black-Scholes closed-form price across simulation counts from 10 to 10,000, demonstrating that MC converges to BS as $N \to \infty$.

---

## Scripts Overview

| Script | What It Produces |
|--------|-----------------|
| `black_scholes_pricing.py` | Compares BS theoretical price to live SPY market price |
| `greeks_visualization.py` | 2x2 plot of Delta, Gamma, Theta, Vega vs stock price |
| `implied_volatility.py` | IV smile curve for calls and puts from live options chain |
| `historical_volatility.py` | SPY price history, log return distribution, 21-day rolling vol |
| `monte_carlo.py` | Single GBM path, 100 simulated paths, MC vs BS convergence |

All plots are saved automatically to the `outputs/` folder.

---

## Setup

**Requirements:** Python 3.9+

```bash
pip install -r requirements.txt
```

**Refresh market data:**
```bash
python src/data_loader.py
```

**Run any script:**
```bash
python scripts/greeks_visualization.py
python scripts/historical_volatility.py
python scripts/monte_carlo.py
python scripts/implied_volatility.py
python scripts/black_scholes_pricing.py
```

**Run tests:**
```bash
pytest tests/
```

---

## Key Results

- **Black-Scholes vs market price difference of $0.22 on calls and $0.04 on puts** for ATM SPY options, validating the implementation against live market data
- **Monte Carlo converges to Black-Scholes** within ~1% by 5,000 simulations, validating the GBM implementation
- **IV smile is visible** across SPY strikes, with higher implied volatility on OTM puts (volatility skew), consistent with the market's demand for downside protection
- **21-day rolling volatility** shows clear volatility clustering: the COVID crash (March 2020) and the 2022 Fed tightening cycle both produced sustained elevated volatility regimes

---

## Limitations & Future Work

- **No dividends:** Black-Scholes as implemented assumes a non-dividend-paying asset. SPY pays a quarterly dividend; a more accurate model would use the continuous dividend yield adjustment: $d_1 = \frac{\ln(S/K) + (r - q + \frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}$
- **Constant volatility:** Black-Scholes assumes $\sigma$ is constant, but the IV smile itself proves it isn't. A natural extension would be a **local volatility** or **Heston stochastic volatility** model
- **American-style exercise:** SPY options are technically American-style. For puts especially, early exercise can matter; a binomial tree or Longstaff-Schwartz Monte Carlo would handle this correctly
- **Data source:** yfinance bid/ask data can be stale for certain strikes. A production system would use a paid data provider (CBOE DataShop, Tradier, Interactive Brokers)