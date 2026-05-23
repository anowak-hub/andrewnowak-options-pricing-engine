# -- Compute option pricing using the Black-Scholes model

# Import Library
import numpy as np 
from scipy.stats import norm

# Define the d1 and d2 quantities 

# d1 
def d1(S, K, T, r, sigma):
    """
    Parameters:
        S = Stock price 
        K = Strike price 
        T = Time left until maturity (years)
        r = Risk free rate 
        sigma = Volatility
    """

    numerator = np.log(S / K) + (r + 0.5 * sigma**2) * T
    denominator = sigma * np.sqrt(T)

    return numerator / denominator

def d2(S, K, T, r, sigma):
    """
    Parameters:
        S = Stock price 
        K = Strike price 
        T = Time left until maturity (years)
        r = Risk free rate 
        sigma = Volatility
    """

    return d1(S, K, T, r, sigma) - sigma*np.sqrt(T)

# Use the d1 and d2 quantities to create the Call and Put Pricing Functions
def call_price(S, K, T, r, sigma):
    # Call Option Pricing 
    return S*norm.cdf(d1(S, K, T, r, sigma)) - K*np.exp(-r*T)*norm.cdf(d2(S, K, T, r, sigma))

def put_price(S, K, T, r, sigma):
    # Put Option pricing 
    return K*np.exp(-r*T)*norm.cdf(-d2(S, K, T, r, sigma)) - S*norm.cdf(-d1(S, K, T, r, sigma))