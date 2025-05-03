# IMPORTANT: RUN THIS CELL IN ORDER TO IMPORT YOUR KAGGLE DATA SOURCES,
# THEN FEEL FREE TO DELETE THIS CELL.
# NOTE: THIS NOTEBOOK ENVIRONMENT DIFFERS FROM KAGGLE'S PYTHON
# ENVIRONMENT SO THERE MAY BE MISSING LIBRARIES USED BY YOUR
# NOTEBOOK.
# import kagglehub
# rpaguirre_tesla_stock_price_path = kagglehub.dataset_download('rpaguirre/tesla-stock-price')
# camnugent_sandp500_path = kagglehub.dataset_download('camnugent/sandp500')
# hershyandrew_amzn_dpz_btc_ntfx_adjusted_may_2013may2019_path = kagglehub.dataset_download('hershyandrew/amzn-dpz-btc-ntfx-adjusted-may-2013may2019')
# tarunpaparaju_apple_aapl_historical_stock_data_path = kagglehub.dataset_download('tarunpaparaju/apple-aapl-historical-stock-data')

print('Data source import complete.')

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

# Input: Stock DataFrame
# Output: Average Daily Return
def get_return(stock_df):
    """
    Function to calculate the daily return of a stock
    """
    daily_returns = stock_df['Close'].pct_change().dropna()
    avg_return = daily_returns.mean()
    return avg_return

def get_correlation(s1_df, s2_df):
    """
    Function to calculate the correlation of the return of two stocks
    """
    returns_1 = s1_df['Close'].pct_change().dropna()
    returns_2 = s2_df['Close'].pct_change().dropna()
    common_index = returns_1.index.intersection(returns_2.index)
    return returns_1.loc[common_index].corr(returns_2.loc[common_index])

def get_covariance(s1_df, s2_df):
    """
    Function to calculate the covariance of the return of two stocks
    """
    returns_1 = s1_df['Close'].pct_change().dropna()
    returns_2 = s2_df['Close'].pct_change().dropna()
    common_index = returns_1.index.intersection(returns_2.index)
    return returns_1.loc[common_index].cov(returns_2.loc[common_index])

def get_votatility(stock_df):
    """
    Function to calculate the volatility of a stock measured by the standard deviation of the daily return
    """
    daily_returns = stock_df['Close'].pct_change().dropna()
    return daily_returns.std()