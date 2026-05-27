# -- File that computes important values such as Delta, Gamma, Vega, Theta, and Rho

# Import 
import numpy as np 
from scipy.stats import norm  

from src.black_scholes import d1, d2

# Compute Delta 
def call_delta(S, K, T, r, sigma):
    return norm.cdf(d1(S, K, T, r, sigma))

def put_delta(S, K, T, r, sigma):
    return norm.cdf(d1(S, K, T, r, sigma)) - 1

# Compute Gamma 
def gamma(S, K, T, r, sigma):
    return (norm.pdf(d1(S, K, T, r, sigma)))/(S*sigma*np.sqrt(T))

# Compute Vega 
def vega(S, K, T, r, sigma):
    return S*np.sqrt(T)*norm.pdf(d1(S, K, T, r, sigma))

# Compute Theta 
def call_theta(S, K, T, r, sigma):
    term1 = -((S*norm.pdf(d1(S, K, T, r, sigma))*sigma) / (2*np.sqrt(T)))
    term2 = -r*K*np.exp(-r*T)*norm.cdf(d2(S, K, T, r, sigma))
    return (term1 + term2) / 252 # Accounts for daily Theta for total number of open market days per year 

def put_theta(S, K, T, r, sigma):
    term1 = -(S*norm.pdf(d1(S, K, T, r, sigma))*sigma) / (2*np.sqrt(T))
    term2 = r*K*np.exp(-r*T)*norm.cdf(-d2(S, K, T, r, sigma))
    return (term1 + term2) / 252 # Accounts for daily Theta for total number of open market days per year 

# Compute Rho
def call_rho(S, K, T, r, sigma):
    D2 = d2(S, K, T, r, sigma)
    return K*T*np.exp(-r*T)*norm.cdf(D2)

def put_rho(S, K, T, r, sigma):
    D2 = d2(S, K, T, r, sigma)
    return -K*T*np.exp(-r*T)*norm.cdf(-D2)