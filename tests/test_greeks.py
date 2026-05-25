# -- Official Automated Testing File for Computing the Greek Values 

# Import 
import sys 
import os
sys.path.append(os.path.abspath("."))

from src.greeks import (
    call_delta,
    put_delta, 
    gamma, 
    vega, 
    call_theta,
    put_theta,
    call_rho,
    put_rho
)

# Test Values 
S = 100 
K = 100
T = 1 
r = 0.05
sigma = 0.2

# Test Delta 
def test_call_delta():
    result = call_delta(S, K, T, r, sigma)
    assert round(result, 4) == 0.6368

def test_put_delta():
    result = put_delta(S, K, T, r, sigma)
    assert round(result, 4) == -0.3632

# Test Gamma
def test_gamma():
    result = gamma(S, K, T, r, sigma)
    assert round(result, 4) == 0.0188

# Test Vega 
def test_vega():
    result = vega(S, K, T, r, sigma)
    assert round(result, 4) == 37.5240

# Test Theta 
def test_call_theta():
    result = call_theta(S, K, T, r, sigma)
    assert round(result, 4) == -0.0255 # Accounts for daily Theta

def test_put_theta():
    result = put_theta(S, K, T, r, sigma)
    assert round(result, 4) == -0.0066 # Accounts for daily Theta

# Test Rho 
def test_call_rho():
    result = call_rho(S, K, T, r, sigma)
    assert round(result, 4) == 53.2325

def test_put_rho():
    result = put_rho(S, K, T, r, sigma)
    assert round(result, 4) == -41.8905

# Call All Test Functions 
test_call_delta()
test_put_delta()
test_gamma()
test_vega()
test_call_theta()
test_put_theta()
test_call_rho()
test_put_rho()
