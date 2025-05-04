from functions import *

# For time stamps
from datetime import datetime
# Set up End and Start times for data grab, starts from 1 year ago to today
end = datetime.now()
start = datetime(end.year - 10, end.month, end.day)
    
# The stocks we'll use for this analysis
company_list = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA', 'NFLX', 'META', 'NVDA', 'AMD', 'INTC']
# company_list = [
#     'AAPL', 'MSFT', 'GOOG', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'PEP', 'COST',
#     'CSCO', 'AVGO', 'ADBE', 'CMCSA', 'TXN', 'INTC', 'QCOM', 'AMD', 'AMGN', 'INTU',
#     'NFLX', 'PYPL', 'SBUX', 'BKNG', 'MDLZ', 'ISRG', 'ADI', 'VRTX', 'MU', 'LRCX',
#     'REGN', 'CSX', 'GILD', 'KLAC', 'BIIB', 'ADP', 'ASML', 'MAR', 'CHTR',
#     'MCHP', 'MNST', 'EXC', 'CTSH', 'CDNS', 'ILMN', 'ROST', 'EA', 'NXPI', 'IDXX',
#     'WBA', 'FAST', 'CTAS', 'BIDU', 'WDAY', 'XEL', 'NTES', 'DLTR', 'PCAR',
#     'PAYX', 'VRSK', 'ALGN', 'EBAY', 'LULU', 'ORLY', 'SIRI', 'TTWO', 'SWKS',
#     'ULTA', 'TTD', 'JD', 'ZM', 'DOCU', 'ZS', 'SNPS', 'TEAM', 'OKTA', 'CRWD', 'MDB',
#     'PANW', 'FTNT', 'DDOG', 'PLTR', 'ABNB', 'ROKU', 'BKR', 'CEG', 'HON', 'GEHC',
#     'AXON', 'MELI', 'PDD', 'GFS', 'ON', 'ODFL', 'CSGP', 'CPRT', 'WBD', 'KDP'
# ]
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

M = get_covariance_matrix(company_list, start, end)
cov_dict = M.to_dict()

# print(stock_return_map)
# print(stock_stdev_map)
# print(cov_dict)

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
portfolio_return = 0
portfolio_volatility = 0
for i in range(n):
    output += f"{company_list[i]}: {x[i] * budget}\n"
with open("out.csv", "w") as f:
    f.write(output)

# Calculate expected portfolio return
portfolio_return = sum(x[i] * stock_return_map[company_list[i]] for i in range(n))

# Convert weights to 1D array for matrix multiplication
weights = np.array(x).reshape((n, 1))

# Convert covariance matrix to numpy array
cov_matrix = np.array([[cov_dict[company_list[i]][company_list[j]] for j in range(n)] for i in range(n)])

# Calculate portfolio variance and volatility (std)
portfolio_variance = (weights.T @ cov_matrix @ weights)[0, 0]
portfolio_volatility = np.sqrt(portfolio_variance)

# Append results to output
output += f"\nExpected Portfolio Return (daily) %: {portfolio_return}\n"
output += f"Expected Portfolio Volatility (daily) %: {portfolio_volatility}\n"

# Write final output to file
with open("out.csv", "w") as f:
    f.write(output)
