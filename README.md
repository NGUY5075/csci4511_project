# 📈 AI-Based Stock Portfolio Optimization with MPT + Backtracking

This project combines **Modern Portfolio Theory (MPT)** with **backtracking algorithms** to build realistic stock portfolios using historical data. The system allows users to optimize their investment strategy based on their **risk aversion level** and automatically handles **realistic constraints** such as integer share allocations and budget limits.

---

## 📂 File Structure

### `main.py`

The main driver script:

- Fetches 1 year of historical stock data from Yahoo Finance for a selected list of companies.
- Computes expected returns, standard deviations, and the covariance matrix.
- Solves two portfolio optimization problems:
  - **Mean-Variance Optimal Portfolio** (maximize utility)
  - **Minimum Variance Portfolio** (minimize total risk)
- Uses **cvxpy** to get theoretical weight allocations.
- Converts weights into share quantities using **custom backtracking algorithms**.
- Generates:
  - `returns.csv`, `cov.csv`, `price.csv`: Stock statistics
  - `out.csv`: Optimization results and summaries
  - `portfolio_comparison.png`: Allocation bar plot
  - `portfolio_shares_comparison.png`: Share allocation bar plot

### `functions.py`

Contains helper functions for:

- Calculating daily return and volatility
- Getting latest closing price
- Computing covariance matrix
- Solving both mean-variance and minimum variance optimization problems using `cvxpy`

### `search.py`

Implements the **backtracking algorithms** for:

- Converting MPT weights into actual share numbers (integer only)
- Maximizing portfolio utility (mean-variance)
- Minimizing portfolio risk (variance)

These algorithms ensure that:

- The total cost stays within the user's budget
- Only realistic, whole-share investments are made

---

## ⚙️ How to Run

1. Install required libraries:

```bash
pip install yfinance pandas numpy matplotlib seaborn cvxpy setuptools
```

2. Run the main script:
python main.py

3. Outputs will be saved as:

- out.csv: Summary of portfolio returns, risks, and share allocations
- portfolio_comparison.png: Bar plot of investment dollars
- portfolio_shares_comparison.png: Bar plot of actual shares to buy

> This coding section was developed with the assistance of OpenAI's ChatGPT, which provided support in code structuring, optimization logic, and documentation writing.
