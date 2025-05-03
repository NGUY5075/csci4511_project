# import numpy as np
from functions import *

# ---------------------------FOR TESTING PURPOSES ONLY------------------------

# For time stamps
from datetime import datetime
# Set up End and Start times for data grab, starts from 1 year ago to today
end = datetime.now()
start = datetime(end.year - 1, end.month, end.day)
    
# The stocks we'll use for this analysis
company_list = ['AAPL', 'GOOG', 'MSFT', 'AMZN']
n = len(company_list)
budget = 1000000

# Download the data from Yahoo Finance
for stock in company_list:
    globals()[stock] = yf.download(stock, start, end)

# Gather data for each stock and write to CSV
stocks_return_string = "Average Daily Return of Stocks\n"
stocks_stdev_string = "Standard Deviation of Stocks' Return\n"
for company in company_list:
    # globals()[company]["company_name"] = com_name
    # globals()[company].to_csv(f"{company}.csv")
    stocks_return_string += get_return(globals()[company]).to_string().split("\n")[1] + "\n"
    stocks_stdev_string += get_votatility(globals()[company]).to_string().split("\n")[1] + "\n"

with open("returns.csv", "w") as f:
    f.write(stocks_return_string)
with open("stdev.csv", "w") as f:
    f.write(stocks_stdev_string)


# ----------------------------REAL CODE---------------------------------
# # A: Risk aversion coefficient in Modern Portfolio Theory (MPT)
# # --------------------------------------------------------------
# # This scalar represents the investor's tolerance for risk:
# # - A lower A (e.g., 1) indicates an aggressive investor who accepts high risk for higher returns.
# # - A moderate A (e.g., 3) reflects balanced risk and return preferences.
# # - A higher A (e.g., 5 or more) indicates a conservative investor who strongly dislikes risk.
# A = 1
# returns = []
# covs = []
# std_devs = []
# weights = []
# stock_map = {}
# cov_map = {}

# # Calculate the expected returns, standard deviations, and covariances
# for i in range(n):
#     stock = stocks_list[i]
#     returns.append(get_return(globals()[stock]))
#     std_devs.append(np.std(globals()[stock]['Adj Close'].pct_change()))
#     weights.append(1/n)
#     stock_map[stock] = i



