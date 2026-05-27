# -- File that contains the Monte Carlo model that simulates stock price evolution 

# Import 
import numpy as np 
from scipy.stats import norm

# Simulate the Stock Path 
def simulate_stock_path(S, T, r, sigma, steps):
    dt = T / steps
    prices = [S]

    for i in range(steps):
        Z = np.random.normal()

        next_price = prices[-1] * np.exp(
            (r - 0.5*sigma**2)*dt
            + (sigma*np.sqrt(dt)*Z)
            )
        
        prices.append(next_price)

    return prices

# Simulate Multiple Stock Paths
def simulate_multiple_paths(S, T, r, sigma, steps, num_simulations):
    all_paths = []

    for i in range(num_simulations):
        path = simulate_stock_path(S, T, r, sigma, steps)
        all_paths.append(path)
    
    return all_paths

# Payoffs for Calls and Puts
def call_payoff(ST,K):
    return max(ST-K, 0)

def put_payoff(ST, K):
    return max(K-ST,0)

# Using the Monte Carlo model for option pricing
def monte_carlo_call_price(S, K, T, r, sigma, steps, num_simulations):
    payoffs = []

    for i in range(num_simulations):
        path = simulate_stock_path(S, T, r, sigma, steps)

        ST = path[-1]

        payoff = max(ST-K, 0)

        payoffs.append(payoff)
    
    average_payoff = np.mean(payoffs)
    return np.exp(-r*T) * average_payoff

def monte_carlo_put_price(S, K, T, r, sigma, steps, num_simulations):
    payoffs = []

    for i in range(num_simulations):
        path = simulate_stock_path(S, T, r, sigma, steps)

        ST = path[-1]

        payoff = max(K-ST, 0)

        payoffs.append(payoff)
    
    average_payoff = np.mean(payoffs)
    return np.exp(-r*T) * average_payoff