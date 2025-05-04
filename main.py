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

stock_map = {}
cov_map = {}
corr_map = {}

# Download the data from Yahoo Finance
for stock in company_list:
    globals()[stock] = yf.download(stock, start, end)

# Gather data for each stock and write to CSV
stocks_return_string = "Average Daily Return of Stocks\n"
stocks_stdev_string = "Standard Deviation of Stocks' Return\n"
for company in company_list:
    stock_map[company] = {}
    return_str = get_return(globals()[company]).to_string().split("\n")[1]
    stdev_str = get_votatility(globals()[company]).to_string().split("\n")[1]
    stocks_return_string += return_str + "\n"
    stocks_stdev_string += stdev_str + "\n"
    stock_map[company]['return'] = return_str.split()[1]
    stock_map[company]['stdev'] = stdev_str.split()[1]
# print(stock_map)

for c1 in company_list:
    for c2 in company_list:
        cov_map[c1 + "/" + c2] = get_covariance(globals()[c1], globals()[c2])
        corr_map[c1 + "/" + c2] = get_correlation(globals()[c1], globals()[c2])


# Write the data to CSV files
with open("returns.csv", "w") as f:
    f.write(stocks_return_string)
with open("stdev.csv", "w") as f:
    f.write(stocks_stdev_string)
