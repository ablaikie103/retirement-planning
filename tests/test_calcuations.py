import unittest
from calculations import calculate_taxable_social_security_benefits, calculate_tax_liability, calculate_long_term_capital_gains_tax_liability       

class TestCalculateTaxableSocialSecurityBenefits(unittest.TestCase):
    def setUp(self):
        self.social_security_thresholds = {'base_amount': 25000, 'phaseout': 15000}

    def test_combined_income_below_base_amount(self):
        social_security_benefits = 20000
        combined_income = 20000
        expected_taxable_amount = 0
        self.assertEqual(calculate_taxable_social_security_benefits(combined_income, self.social_security_thresholds, social_security_benefits), expected_taxable_amount)

    def test_combined_income_within_phaseout_range(self):
        social_security_benefits = 20000
        combined_income = 35000
        expected_taxable_amount = 10000 * 0.5
        self.assertEqual(calculate_taxable_social_security_benefits(combined_income, self.social_security_thresholds, social_security_benefits), expected_taxable_amount)

    def test_combined_income_above_phaseout_range(self):
        social_security_benefits = 20000
        combined_income = 50000
        expected_taxable_amount = 15000 * 0.5 + (combined_income - 25000 - 15000) * 0.85
        self.assertEqual(calculate_taxable_social_security_benefits(combined_income, self.social_security_thresholds, social_security_benefits), expected_taxable_amount)

    def test_taxable_amount_greater_than_85_percent_of_benefits(self):
        social_security_benefits = 10000
        combined_income = 50000
        expected_taxable_amount = 8500
        self.assertEqual(calculate_taxable_social_security_benefits(combined_income, self.social_security_thresholds, social_security_benefits), expected_taxable_amount)


class TestCalculateTaxLiability(unittest.TestCase):
    def setUp(self):
        self.tax_brackets = [{'lower_limit': 0, 'upper_limit': 10000, 'tax_rate': 0.1},
                             {'lower_limit': 10000, 'upper_limit': 50000, 'tax_rate': 0.2},
                             {'lower_limit': 50000, 'upper_limit': float('inf'), 'tax_rate': 0.3}]
    
    def test_tax_liability_with_no_income(self):
        income = 0
        expected_tax_liability = 0
        self.assertEqual(calculate_tax_liability(income, self.tax_brackets), expected_tax_liability)

    def test_tax_liability_with_income_in_first_tax_bracket(self):
        income = 5000
        expected_tax_liability = 500
        self.assertEqual(calculate_tax_liability(income, self.tax_brackets), expected_tax_liability)
        
    def test_tax_liability_with_income_in_second_tax_bracket(self):
        income = 15000
        expected_tax_liability = 1000 + 5000 * 0.2
        self.assertEqual(calculate_tax_liability(income, self.tax_brackets), expected_tax_liability)
       
        
    def test_tax_liability_with_income_above_upper_limit(self):
        income = 100000
        expected_tax_liability = 10000*0.1+40000*0.2+50000*0.3
        self.assertEqual(calculate_tax_liability(income, self.tax_brackets), expected_tax_liability)


class TestCalculateLongTermCapitalGainsTaxLiability(unittest.TestCase):
    def setUp(self):
        self.tax_brackets = [{"lower_limit": 0, "upper_limit": 10000, "tax_rate": 0.1},
                             {"lower_limit": 10000, "upper_limit": 20000, "tax_rate": 0.2},
                             {"lower_limit": 20000, "upper_limit": float('inf'), "tax_rate": 0.3}]

    def test_no_capital_gains(self):
        taxable_income = 50000
        capital_gains = 0
        expected_tax_liability = 0
        self.assertAlmostEqual(calculate_long_term_capital_gains_tax_liability(taxable_income, capital_gains, self.tax_brackets), expected_tax_liability)

    def test_capital_gains_below_bracket(self):
        taxable_income = 1000
        capital_gains = 5000
        expected_tax_liability = 500
        self.assertAlmostEqual(calculate_long_term_capital_gains_tax_liability(taxable_income, capital_gains, self.tax_brackets), expected_tax_liability)

    def test_capital_gains_within_bracket(self):
        taxable_income = 1000
        capital_gains = 15000
        expected_tax_liability = 900+(15000-9000)*0.2
        self.assertAlmostEqual(calculate_long_term_capital_gains_tax_liability(taxable_income, capital_gains, self.tax_brackets), expected_tax_liability)

    def test_capital_gains_above_bracket(self):
        taxable_income = 50000
        capital_gains = 50000
        expected_tax_liability = capital_gains*0.3
        self.assertAlmostEqual(calculate_long_term_capital_gains_tax_liability(taxable_income, capital_gains, self.tax_brackets), expected_tax_liability)

    def test_no_tax_brackets(self):
        taxable_income = 50000
        capital_gains = 50000
        tax_brackets = []
        expected_tax_liability = 0
        self.assertAlmostEqual(calculate_long_term_capital_gains_tax_liability(taxable_income, capital_gains, tax_brackets), expected_tax_liability)


if __name__ == "__main__":
    unittest.main()