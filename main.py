# import numpy as np
from functions import *
# stocks_list = ['AAPL', 'GOOG', 'MSFT', 'AMZN']
# company_name = ["APPLE", "GOOGLE", "MICROSOFT", "AMAZON"]
# n = len(stocks_list)
# budget = 1000000

# For testing purposes
# For time stamps
from datetime import datetime

# The tech stocks we'll use for this analysis
# tech_list = ['AAPL', 'GOOG', 'MSFT', 'AMZN']

# Set up End and Start times for data grab
# tech_list = ['AAPL', 'GOOG', 'MSFT', 'AMZN']

end = datetime.now()
start = datetime(end.year - 1, end.month, end.day)
    

company_list = ['AAPL', 'GOOG', 'MSFT', 'AMZN']
company_name = ["APPLE", "GOOGLE", "MICROSOFT", "AMAZON"]
# company_list = ['AAPL']
# company_name = ["APPLE"]

for stock in company_list:
    globals()[stock] = yf.download(stock, start, end)
    # print(globals()[stock])

for company, com_name in zip(company_list, company_name):
    globals()[company]["company_name"] = com_name
    globals()[company].to_csv(f"{company}.csv")
    print(get_return(globals()[company]))


# Real thing starts here
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



