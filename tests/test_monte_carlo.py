# -- Official Automated Testing File for the Monte Carlo Model

# Import 
import numpy as np
import sys 
import os
sys.path.append(os.path.abspath("."))

from src.monte_carlo import (
    simulate_stock_path,
    simulate_multiple_paths, 
    call_payoff, 
    put_payoff,
    monte_carlo_call_price, 
    monte_carlo_put_price
)

# Test Parameters 
S = 100
K = 100
T = 1
r = 0.05
sigma = 0.2 
steps = 252
num_simulations = 10000

# Test the Option Prices
def test_monte_carlo_call_price():
    np.random.seed(42)
    result = monte_carlo_call_price(S, K, T, r, sigma, steps, num_simulations)
    assert abs(result - 10.45) < 0.5

def test_monte_carlo_put_price():
    np.random.seed(42)
    result = monte_carlo_put_price(S, K, T, r, sigma, steps, num_simulations)
    assert abs(result - 5.57) < 0.6

# Call Test Functions 
test_monte_carlo_call_price()
test_monte_carlo_put_price()