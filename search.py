# backtracking_solver.py
import numpy as np
import itertools

# Prepare *NUMBER OF SHARES* options per stock based on MPT weights
def generate_share_options(mpt_weights, stock_prices, budget):
    options = []
    for i in range(len(stock_prices)):
        ideal_dollar = mpt_weights[i] * budget
        ideal_shares = ideal_dollar / stock_prices[i]
        floor_shares = max(int(np.floor(ideal_shares)), 0)
        ceil_shares = int(np.ceil(ideal_shares))
        options.append([floor_shares, ceil_shares])
    return options

# Backtracking to maximize mean-variance utility

def backtrack_mean_variance(
    index,
    current_combo,
    current_cost,
    budget,
    options,
    stock_prices,
    expected_returns,
    cov_matrix,
    A,
    best_solution,
    best_utility
):
    n = len(stock_prices)

    if index == n:
        if current_cost <= budget:
            investments = np.array(current_combo) * stock_prices
            weights = investments / np.sum(investments)
            port_return = np.dot(weights, expected_returns)
            variance = np.dot(weights.T, np.dot(cov_matrix, weights))
            utility = port_return - A * variance
            if utility > best_utility[0]:
                best_utility[0] = utility
                best_solution[0] = list(current_combo)
        return

    for shares in options[index]:
        new_cost = current_cost + shares * stock_prices[index]
        if new_cost > budget:
            continue
        backtrack_mean_variance(
            index + 1,
            current_combo + [shares],
            new_cost,
            budget,
            options,
            stock_prices,
            expected_returns,
            cov_matrix,
            A,
            best_solution,
            best_utility
        )

# Backtracking to minimize total portfolio variance

def backtrack_min_variance(
    index,
    current_combo,
    current_cost,
    budget,
    options,
    stock_prices,
    cov_matrix,
    best_solution,
    best_variance
):
    n = len(stock_prices)

    if index == n:
        if current_cost <= budget:
            investments = np.array(current_combo) * stock_prices
            weights = investments / np.sum(investments)
            variance = np.dot(weights.T, np.dot(cov_matrix, weights))
            if variance < best_variance[0]:
                best_variance[0] = variance
                best_solution[0] = list(current_combo)
        return

    for shares in options[index]:
        new_cost = current_cost + shares * stock_prices[index]
        if new_cost > budget:
            continue
        backtrack_min_variance(
            index + 1,
            current_combo + [shares],
            new_cost,
            budget,
            options,
            stock_prices,
            cov_matrix,
            best_solution,
            best_variance
        )
