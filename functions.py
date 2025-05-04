import pandas as pd
import numpy as np

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
    """
    daily_returns = stock_df['Close'].pct_change().dropna()
    return daily_returns.std()

def get_correlation(s1_df, s2_df):
    """
    Function to calculate the correlation of the return of two stocks
    """
    returns_1 = s1_df['Close'].pct_change().dropna()
    returns_2 = s2_df['Close'].pct_change().dropna()
    return returns_1.corr(returns_2)

def get_covariance(s1_df, s2_df):
    """
    Function to calculate the covariance of the return of two stocks
    """
    returns_1 = s1_df['Close'].astype(float).pct_change().dropna()
    returns_2 = s2_df['Close'].astype(float).pct_change().dropna()
    return returns_1.cov(returns_2)
