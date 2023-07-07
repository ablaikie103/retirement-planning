import unittest
import numpy as np
from models import calculate_withdrawal_for_spending, simulate_stock_returns

class TestWithdrawalCalculation(unittest.TestCase):
    
    def test_calculate_withdrawal_for_spending(self):
        # Test case 1
        spending = 10000
        social_security = 0
        capital_gains = 0
        filing_status = 'single'
        expected_result = 12500 # Assuming tax rate is flat 20%
        def calculate_taxes_func(withdrawal, capital_gains, social_security, filing_status):
            taxes = 0.2*(withdrawal + capital_gains +social_security)
            return taxes, taxes/(withdrawal)
        result = calculate_withdrawal_for_spending(spending, social_security, capital_gains, filing_status, calculate_taxes_func, accuracy=0.001)
        self.assertAlmostEqual(result, expected_result, places=2)



class TestStockReturnsSimulation(unittest.TestCase):
    def test_stock_means(self):
        stock_mean = 0.05
        stock_std = 0.1
        bond_mean = 0.02
        bond_std = 0.15
        correlation = 0.5

        simulate_func = simulate_stock_returns(stock_mean, stock_std, bond_mean, bond_std, correlation)
        num_trials = 100000
        stock_returns = np.zeros(num_trials)
        bond_returns = np.zeros(num_trials)

        for i in range(num_trials):
            simulated_returns = simulate_func()
            stock_returns[i] = simulated_returns[0]
            bond_returns[i] = simulated_returns[1]

        simulated_stock_return = np.mean(stock_returns)
        simulated_bond_return = np.mean(bond_returns)
        simulated_stock_std = np.std(stock_returns)
        simulated_bond_std = np.std(bond_returns)
        simulated_correlation = np.corrcoef(stock_returns, bond_returns)[0][1]

        # Check if the simulation averages match the output of the function
        self.assertAlmostEqual(simulated_stock_return, stock_mean, delta=0.01)
        self.assertAlmostEqual(simulated_bond_return, bond_mean, delta=0.01)
        self.assertAlmostEqual(simulated_stock_std, stock_std, delta=0.01)
        self.assertAlmostEqual(simulated_bond_std, bond_std, delta=0.01)
        self.assertAlmostEqual(simulated_correlation, correlation, delta=0.01)


if __name__ == '__main__':
    unittest.main()
