from functions import *

# For time stamps
from datetime import datetime
# Set up End and Start times for data grab, starts from 1 year ago to today
end = datetime.now()
start = datetime(end.year - 1, end.month, end.day)
    
# The stocks we'll use for this analysis
company_list = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA', 'NFLX', 'META', 'NVDA', 'AMD', 'INTC']
n = len(company_list)
budget = 1000000

# A: Risk aversion coefficient in Modern Portfolio Theory (MPT)
# --------------------------------------------------------------
# This scalar represents the investor's tolerance for risk:
# - A lower A (e.g., 1) indicates an aggressive investor who accepts high risk for higher returns.
# - A moderate A (e.g., 3) reflects balanced risk and return preferences.
# - A higher A (e.g., 5 or more) indicates a conservative investor who strongly dislikes risk.
A = 1

stock_return_map = {}
stock_stdev_map = {}
cov_map = {}
corr_map = {}

# Download the data from Yahoo Finance
for stock in company_list:
    globals()[stock] = yf.download(stock, start, end)

# Gather data for each stock and write to CSV
stocks_return_string = "Average Daily Return of Stocks\n"
stocks_stdev_string = "Standard Deviation of Stocks' Return\n"
for company in company_list:
    return_str = get_return(globals()[company]).to_string().split("\n")[1]
    stdev_str = get_votatility(globals()[company]).to_string().split("\n")[1]
    stocks_return_string += return_str + "\n"
    stocks_stdev_string += stdev_str + "\n"
    stock_return_map[company] = return_str.split()[1]
    stock_stdev_map[company] = stdev_str.split()[1]

M = get_covariance_matrix(company_list, start, end)
cov_dict = M.to_dict()

# print(stock_return_map)
# print(stock_stdev_map)
# print(cov_dict)

# Write the data to CSV files
with open("returns.csv", "w") as f:
    f.write(stocks_return_string)
with open("stdev.csv", "w") as f:
    f.write(stocks_stdev_string)
with open("cov.csv", "w") as f:
    f.write(M.to_string())
