# -- File That Computes the Historical and Implied Volatility

# Import 
import numpy as np 
from scipy.stats import norm

import pandas as pd

from src.black_scholes import call_price, put_price
from src.greeks import vega

# Historical Volatility
def historical_volatility(prices):
    returns = np.log(prices/prices.shift(1))
    returns = returns.dropna()

    volatility = returns.std()*np.sqrt(252)

    return volatility

# Implied Volatility
def implied_volatility_call(market_price, S, K, T, r, sigma=0.2, tolerance=1e-5, max_iterations=100):
    for i in range(max_iterations):
        model_price = call_price(S, K, T, r, sigma)
        vega_value = vega(S, K, T, r, sigma)

        error = model_price - market_price

        if abs(error) < tolerance:
            return sigma

        sigma = error - error / vega_value
    
    return sigma

def implied_volatility_put(market_price, S, K, T, r, sigma=0.2, tolerance=1e-5, max_iterations=100):
    for i in range(max_iterations):
        model_price = put_price(S, K, T, r, sigma)
        vega_value = vega(S, K, T, r, sigma)

        error = model_price - market_price

        if abs(error) < tolerance:
            return sigma

        sigma = error - error / vega_value
    
    return sigma
