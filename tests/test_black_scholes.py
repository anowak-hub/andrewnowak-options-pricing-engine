# -- Official Automated Testing File for the Black Scholes Model 

# Import
import sys 
import os 
sys.path.append(os.path.abspath("."))

from src.black_scholes import call_price, put_price

# Test Call Price Method
def test_call_price():
    result = call_price(100, 100, 1, 0.05, 0.2)
    assert round(result, 2) == 10.45

# Test Put Price Method 
def test_put_price():
    result = put_price(100,100,1,0.05,0.2)
    assert round(result, 2) == 5.57

test_call_price()
test_put_price()