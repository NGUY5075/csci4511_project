import pandas as pd
import numpy as np
import cvxpy as cp

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
plt.style.use("fivethirtyeight")
# %matplotlib inline

# For reading stock data from yahoo
from pandas_datareader.data import DataReader
import yfinance as yf
from pandas_datareader import data as pdr

def get_return(stock_df):
    """
    Function to calculate the daily return of a stock
    Input: Stock DataFrame
    Output: Average Daily Return
    Current price: Closing price of the stock at the end of day t
    Previous price: Closing price of the stock at the end of day t-1
    Return = (Current Price - Previous Price) / Previous Price
    """
    daily_returns = stock_df['Close'].pct_change().dropna()
    avg_return = daily_returns.mean()
    return avg_return

def get_votatility(stock_df):
    """
    Function to calculate the volatility of a stock measured by the standard deviation of the daily return
    Input: Stock DataFrame
    Output: Standard Deviation of Return
    """
    daily_returns = stock_df['Close'].pct_change().dropna()
    return daily_returns.std()

def get_closing_price(stock_df):
    """
    Function to get the most recent closing price of a stock
    Input: Stock DataFrame
    Output: Closing Price DataFrame
    """
    return stock_df['Close'].tail(1)

def get_covariance_matrix(stock_list, start, end):
    """
    Returns the covariance matrix of the daily returns of a list of stocks
    """
    closing_df = yf.download(stock_list, start=start, end=end)['Close']
    returns = closing_df.pct_change().dropna()
    return returns.cov()

def solve_mpt_constrained(expected_returns, cov_matrix, A):
    n = len(expected_returns)
    x = cp.Variable(n)
    # Objective: maximize mean-variance utility
    objective = cp.Maximize(x @ expected_returns - A * cp.quad_form(x, cov_matrix))
    # Constraints: weights sum to 1, no short-selling
    constraints = [
        cp.sum(x) == 1,
        x >= 0
    ]
    # Problem
    prob = cp.Problem(objective, constraints)
    prob.solve()
    return x.value

def solve_min_variance_portfolio(cov_matrix):
    """
    Solves for the minimum variance portfolio weights with no short-selling.

    Parameters:
    cov_matrix (numpy.ndarray): The covariance matrix of asset returns.

    Returns:
    numpy.ndarray: Optimal asset weights minimizing portfolio variance.
    """
    n = cov_matrix.shape[0]
    w = cp.Variable(n)
    # Objective: Minimize portfolio variance
    objective = cp.Minimize(cp.quad_form(w, cov_matrix))
    # Constraints: weights sum to 1, no short-selling
    constraints = [
        cp.sum(w) == 1,
        w >= 0
    ]
    # Problem
    prob = cp.Problem(objective, constraints)
    prob.solve()
    return w.value
