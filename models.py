import numpy as np
from calculations import calculate_federal_taxes
import matplotlib.pyplot as plt
import json


def calculate_withdrawal_for_spending(spending, social_security, capital_gains, filing_status, calculate_taxes_func, accuracy=1):
    """
    Calculate the withdrawal amount required for spending, taking into account federal taxes.
    Args:
        spending (float): The desired spending amount.
        social_security (float): The social security amount.
        capital_gains (float): The capital gains amount.
        filing_status (str): The filing status for tax calculation.
        calculate_taxes_func (function): The function to calculate federal taxes.
        accuracy (float, optional): The desired accuracy for the withdrawal amount. Defaults to 1.
    Returns:
        float: The withdrawal amount required for the given spending amount.
    """
    taxes, rate = calculate_taxes_func(spending, capital_gains, social_security, filing_status)
    withdrawal = spending + taxes
    diff = abs(spending - withdrawal)
    while diff > accuracy:
        taxes, rate = calculate_taxes_func(withdrawal, capital_gains, social_security, filing_status)
        new_withdrawal = spending + taxes
        diff = abs(new_withdrawal - withdrawal)
        withdrawal = new_withdrawal
    return withdrawal


def simulate_stock_returns(mean1, std1, mean2, std2, correlation):
    """
    Simulate stock returns based on mean, standard deviation, and correlation.
    
    Args:
        mean1 (float): Mean of the first stock's returns.
        std1 (float): Standard deviation of the first stock's returns.
        mean2 (float): Mean of the second stock's returns.
        std2 (float): Standard deviation of the second stock's returns.
        correlation (float): Correlation between the two stocks' returns.
    
    Returns:
        function: A function that can be called to simulate stock returns.
    """
    covariance = correlation * std1 * std2
    covariance_matrix = [[std1**2, covariance], [covariance, std2**2]]
    mean = [mean1, mean2]
    
    def simulate():
        return np.random.multivariate_normal(mean, covariance_matrix)
    
    return simulate

def monte_carlo_simulation(starting_amount, spending, deposit, years, w1, plot=False):
    with open('configs/market_returns.json', 'r') as f:
        config = json.load(f)
        mean1 = config['stock_returns']
        std1 = config['stock_std']
        mean2 = config['bond_returns']
        std2 = config['bond_std']
        correlation = config['correlation']
    
    price_series = np.zeros(years)
    price_series[0] = starting_amount
    simulate_func = simulate_stock_returns(mean1, std1, mean2, std2, correlation)

    for i in range(1, years):
        simulated_returns1, simulated_returns2 = simulate_func()
        yearly_returns = w1 * simulated_returns1 + (1 - w1) * simulated_returns2
        price_series[i] = price_series[i - 1] * (1+yearly_returns)
        withdrawal = calculate_withdrawal_for_spending(spending, 0, 0, 'single', calculate_federal_taxes)
        price_series[i] = max(price_series[i] - withdrawal, 0)

    if plot:
        plt.plot(price_series)
        plt.xlabel('Years')
        plt.ylabel('Portfolio Value')
        plt.title('Monte Carlo Simulation')
        plt.show()
    return price_series

def run_monte_carlo_simulation(starting_amount, spending, deposit, years, stock_weight, num_simulations=100):

    pass_count = 0
    fail_count = 0
    ending_value_sum = 0
    for i in range(num_simulations):
        price_series = monte_carlo_simulation(starting_amount, spending, deposit, years, stock_weight)
        if price_series[-1] > 0:
            pass_count += 1
            ending_value_sum += price_series[-1]
        else:
            fail_count += 1
    
    pass_percentage = pass_count / num_simulations * 100
    fail_percentage = fail_count / num_simulations * 100
    ending_value = ending_value_sum / pass_count
    print(f"Pass percentage: {pass_percentage:.2f}%")
    print(f"Fail percentage: {fail_percentage:.2f}%")
    print(f"Average ending value: {ending_value:.2f}")

    return pass_percentage, fail_percentage

print(run_monte_carlo_simulation(1000000, 50000, 0, 30, 0.5, 100))