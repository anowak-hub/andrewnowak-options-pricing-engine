# -- Automated Testing File for Computing Volatility

# Import
import sys
import os

sys.path.append(os.path.abspath(".."))

import numpy as np
import pandas as pd

from src.volatility import (
    historical_volatility,
    implied_volatility_call,
    implied_volatility_put
)

from src.black_scholes import (
    call_price,
    put_price
)

# Test Historical Volatility
def test_historical_volatility():
    prices = pd.Series([
        100,
        101,
        102,
        100,
        103
    ])

    result = historical_volatility(prices)
    
    assert result > 0

# Test Implied Volatility

def test_implied_volatility_call():
    sigma_true = 0.2

    market_price = call_price(100, 100, 1, 0.05, sigma_true)

    iv = implied_volatility_call(market_price, 100, 100, 1, 0.05)

    assert abs(iv - sigma_true) < 1e-3

def test_implied_volatility_put():
    sigma_true = 0.2

    market_price = put_price(100, 100, 1, 0.05, sigma_true)

    iv = implied_volatility_put(market_price, 100, 100, 1, 0.05)

    assert abs(iv - sigma_true) < 1e-3