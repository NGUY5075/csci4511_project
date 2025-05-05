from functions import *
from search import *
import matplotlib.pyplot as plt

# For time stamps
from datetime import datetime
# Set up End and Start times for data grab, starts from 1 year ago to today
end = datetime.now()
start = datetime(end.year - 1, end.month, end.day)
    
# The stocks we'll use for this analysis
company_list = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA', 'NFLX', 'META', 'NVDA', 'AMD', 'INTC']
# Larger list of stocks for a more comprehensive analysis
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
n = len(company_list)
budget = 1000000  # Total budget for the portfolio

# A: Risk aversion coefficient in Modern Portfolio Theory (MPT)
# --------------------------------------------------------------
# This scalar represents the investor's tolerance for risk:
# - A lower A (e.g., 1) indicates an aggressive investor who accepts high risk for higher returns.
# - A moderate A (e.g., 3) reflects balanced risk and return preferences.
# - A higher A (e.g., 5 or more) indicates a conservative investor who strongly dislikes risk.
A = 10

stock_return_map = {}
stock_stdev_map = {}
stock_recent_price_map = {}

# Download the data from Yahoo Finance
for stock in company_list:
    globals()[stock] = yf.download(stock, start, end)

# Gather data for each stock and write to CSV
stocks_return_string = "Average Daily Return of Stocks\n"
stocks_stdev_string = "Standard Deviation of Stocks' Return\n"
stocks_price_string = "Most recent closing price of Stocks\n"
closing_prices = []
for company in company_list:
    return_str = get_return(globals()[company]).to_string().split("\n")[1]
    stdev_str = get_votatility(globals()[company]).to_string().split("\n")[1]
    price_str = get_closing_price(globals()[company]).to_string().split("\n")[2]
    # print(price_str)
    # print(price_str.split()[1])
    # price_str = get_closing_price(globals()[company]).to_string().split("\n")[1]
    stocks_return_string += return_str + "\n"
    stocks_stdev_string += stdev_str + "\n"
    stocks_price_string += company + ": " + price_str.split()[1] + "\n"
    # stocks_price_string += price_str + "\n"
    stock_return_map[company] = float(return_str.split()[1])
    stock_stdev_map[company] = float(stdev_str.split()[1])
    stock_recent_price_map[company] = float(price_str.split()[1])
    closing_prices.append(float(price_str.split()[1]))
    # stock_recent_price_map[company] = float(price_str.split()[1])

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
with open("price.csv", "w") as f:
    f.write(stocks_price_string)

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
expected_returns = np.array(list(stock_return_map.values()))
x = solve_mpt_constrained(expected_returns, M, A)
# x = np.linalg.solve(m, b)
# x /= np.sum(x)
output = "--- Mean-Variance Optimal Portfolio ---\n"
portfolio_return = 0
portfolio_volatility = 0

for i in range(n):
    output += f"{company_list[i]}: {round(float(x[i]*budget))}\n"
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
output += f"\nExpected Portfolio Return (daily) %: {round(float(portfolio_return * 100), 3)}\n"
output += f"Expected Portfolio Volatility (daily) %: {round(float(portfolio_volatility * 100), 3)}\n"

# Set up the optimization problem for Minimum Variance Portfolio
# Constraint: sum of weights = 1
# We use the method of Lagrange multipliers to solve:
# Minimize: aᵀ Σ a
# Subject to: 1ᵀ a = 1

# Construct augmented matrix [Σ 1; 1ᵀ 0]
aug_m = np.zeros((n + 1, n + 1))
aug_m[:n, :n] = cov_matrix
aug_m[:n, n] = 1
aug_m[n, :n] = 1

# Construct RHS vector [0...0; 1]
aug_b = np.zeros((n + 1, 1))
aug_b[n, 0] = 1

# Solve for weights and lagrange multiplier
# aug_solution = np.linalg.solve(aug_m, aug_b)
aug_solution = solve_min_variance_portfolio(M)
minvar_weights = aug_solution[:n].reshape((n, 1))

# Expected portfolio return for minimum variance portfolio
minvar_portfolio_return = (minvar_weights.T @ np.array([stock_return_map[company] for company in company_list]).reshape((n, 1))).item()
minvar_portfolio_variance = (minvar_weights.T @ cov_matrix @ minvar_weights).item()
minvar_portfolio_volatility = np.sqrt(minvar_portfolio_variance)

output += "\n--- Minimum Variance Portfolio ---\n"
for i in range(n):
    output += f"{company_list[i]}: {round(minvar_weights[i, 0] * budget)}\n"
output += f"\nMinimum Variance Portfolio Return (daily) %: {round(float(minvar_portfolio_return*100))}\n"
output += f"Minimum Variance Portfolio Volatility (daily) %: {round(float(minvar_portfolio_volatility*100),3)}\n"

with open("out.csv", "w") as f:
    f.write(output)

# Extract allocation values for both portfolios
meanvar_allocations = [float(x[i]) * budget for i in range(n)]
minvar_allocations = [float(minvar_weights[i]) * budget for i in range(n)]

# Set position for bars
indices = np.arange(n)
bar_width = 0.35

# Plotting
plt.figure(figsize=(round(1.4*n), 10))
plt.bar(indices, meanvar_allocations, bar_width, label='Mean-Variance Optimal')
plt.bar(indices + bar_width, minvar_allocations, bar_width, label='Minimum Variance')

# Labels and Titles
plt.xlabel('Stock')
plt.ylabel('Investment Amount ($)')
plt.title('Portfolio Allocations Comparison')
plt.xticks(indices + bar_width / 2, company_list, rotation=45)
plt.legend()
plt.tight_layout()
# Save plot
plt.savefig('portfolio_comparison.png')

# Using backtracking to find the mean variance portfolio
# --------------------------------------------------------------
meanvar_allocations = generate_share_options(x, closing_prices, budget)
# print(meanvar_allocations)

meanvar_solution = [None]
meanvar_utility = [-float("inf")]

backtrack_mean_variance(
    index=0,
    current_combo=[],
    current_cost=0,
    budget=budget,
    options=meanvar_allocations,
    stock_prices=np.array(list(stock_recent_price_map.values())),
    expected_returns=np.array(list(stock_return_map.values())),
    cov_matrix=cov_matrix,
    A=A,
    best_solution=meanvar_solution,
    best_utility=meanvar_utility
)

# Using backtrack to find the minimum variance portfolio
minvar_allocations = generate_share_options(aug_solution, closing_prices, budget)
minvar_solution = [None]
minvar_variance = [float("inf")]
backtrack_min_variance(
    index=0,
    current_combo=[],
    current_cost=0,
    budget=budget,
    options=minvar_allocations,
    stock_prices=np.array(list(stock_recent_price_map.values())),
    cov_matrix=cov_matrix,
    best_solution=minvar_solution,
    best_variance=minvar_variance
)

# Access result:
print("Meanvar portfolio (shares):", meanvar_solution[0])
print("Meanvar utility:", meanvar_utility[0])
print("Minvar portfolio (shares):", minvar_solution[0])
print("Minvar variance:", minvar_variance[0])

# Draw the plot