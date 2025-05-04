from functions import *

# For time stamps
from datetime import datetime
# Set up End and Start times for data grab, starts from 1 year ago to today
end = datetime.now()
start = datetime(end.year - 1, end.month, end.day)
    
# The stocks we'll use for this analysis
company_list = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA', 'NFLX', 'META', 'NVDA', 'AMD', 'INTC']
# n = len(company_list)
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
    stock_return_map[company] = float(return_str.split()[1])
    stock_stdev_map[company] = float(stdev_str.split()[1])

# Filter out all the stocks with negative or zero returns
# positive_companies = []
# for company in company_list:
#     if stock_return_map[company] > 0:
#         positive_companies.append(company)
M = get_covariance_matrix(company_list, start, end)
cov_dict = M.to_dict()

# print(stock_return_map)
# print(stock_stdev_map)
# print(cov_dict)

# Filter out all the stocks with negative returns
n = len(company_list)

# Write the data to CSV files
with open("returns.csv", "w") as f:
    f.write(stocks_return_string)
with open("stdev.csv", "w") as f:
    f.write(stocks_stdev_string)
with open("cov.csv", "w") as f:
    f.write(M.to_string())

# Set up the optimization problem
m = np.zeros((n, n))
b = np.zeros((n, 1))
b[n - 1] = 1

# Fill in the last condition which is the sum of weights = 1
# for i in range(n):
#     m[n - 1][i] = 1
for i in range(n):
    b[i] = stock_return_map[company_list[i]]/A

# Fill in the covariance matrix
for i in range(n):
    for j in range(n):
        m[i][j] = cov_dict[company_list[i]][company_list[j]]

# Solve for x
x = np.linalg.solve(m, b)
x /= np.sum(x)
output = "The optimal amount to invest in the stocks are:\n"
for i in range(n):
    output += f"{company_list[i]}: {x[i] * budget}\n"
with open("out.csv", "w") as f:
    f.write(output)
