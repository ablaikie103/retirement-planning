import json
import numpy as np

SOCIAL_SECURITY_THRESHOLD_FILE = 'configs/social_security_thresholds.json'
INCOME_TAX_BRACKETS_FILE = 'configs/federal_tax_brackets.json'
CAPITAL_GAINS_TAX_BRACKETS_FILE = 'configs/capital_gains_tax_brackets.json'
STANDARD_DEDUCTION = 'configs/federal_standard_deduction.json'

def calculate_taxable_social_security_benefits(combined_income, social_security_thresholds, social_security_benefits):
    """
    Calculates the taxable amount of Social Security benefits based on the combined income, 
    using the base amount and phaseout from the Social Security thresholds.
    
    Args:
    combined_income (float): The combined income, which is the sum of the MAGI and half of the Social Security benefits.
    social_security_thresholds (dict): A dictionary containing the base amount and phaseout for Social Security benefits.
    social_security_benefits (float): The total amount of Social Security benefits received.
    
    Returns:
    float: The taxable amount of Social Security benefits.
    """
    base_amount, phaseout =  social_security_thresholds['base_amount'], social_security_thresholds['phaseout']
    if combined_income < base_amount:
        return 0
    elif combined_income < base_amount + phaseout:
        taxable_amount = (combined_income - base_amount) * 0.5
    else:
        taxable_amount = phaseout * 0.5 + (combined_income - base_amount - phaseout) * 0.85
    return min(0.85 * social_security_benefits, taxable_amount)

def calculate_tax_liability(income, tax_brackets):
    """
    Calculates the tax liability based on the provided income and tax brackets.

    Parameters:
        income (float): The taxable income.
        tax_brackets (list): A list of dictionaries containing the tax brackets.

    Returns:
        float: The tax liability based on the provided income and tax brackets.
    """
    tax_owed = 0
    for bracket in tax_brackets:
        if income > bracket['lower_limit']:
            taxable_income = min(income, bracket['upper_limit']) - bracket['lower_limit']
            tax_owed += taxable_income * bracket['tax_rate']
            if income <= bracket['upper_limit']:
                break
    return tax_owed


def calculate_long_term_capital_gains_tax_liability(taxable_income, capital_gains, tax_brackets):
    """
    Calculates the tax liability on long-term capital gains based on taxable income and tax brackets.
    Args:
    taxable_income (float): The taxable income.
    capital_gains (float): The long-term capital gains.
    tax_brackets (list): A list of dictionaries representing the tax brackets. Each dictionary contains three keys: 
    "lower_limit", "upper_limit", and "tax_rate". The "lower_limit" and "upper_limit" represent the limits of the tax bracket, 
    and the "tax_rate" represents the tax rate for that bracket.
    Returns:
    float: The tax liability on long-term capital gains.
    """
    if capital_gains > 0:
        tax_liability = 0
        for bracket in tax_brackets:
            bracket_upper = bracket["upper_limit"] - taxable_income
            bracket_lower = max(bracket["lower_limit"] - taxable_income, 0)
            if bracket_upper < 0:
                continue
            elif capital_gains > bracket_upper:
                tax_liability += (bracket_upper - bracket_lower) * bracket["tax_rate"]
            elif capital_gains > bracket_lower:
                tax_liability += (capital_gains - bracket_lower) * bracket["tax_rate"]
                break
        return tax_liability
    return 0


def calculate_federal_taxes(regular_income, capital_gains, social_security_benefits, filing_status):
    """
    Calculates the federal taxes owed in retirement based on current tax policies.
    Inputs:
    regular_income (float): Total regular income in retirement.
    capital_gains (float): Total capital gains in retirement.
    social_security_benefits (float): Total social security benefits in retirement.
    filing_status (str): Filing status, either "single" or "married".
    Returns:
    Tuple containing:
    - taxes_owed (float): Total federal taxes owed.
    - effective_tax_rate (float): Effective tax rate.
    """

    with open(INCOME_TAX_BRACKETS_FILE, 'r') as f:
        income_tax_brackets = json.load(f)

    with open(SOCIAL_SECURITY_THRESHOLD_FILE, 'r') as f:
        social_security_thresholds = json.load(f)

    with open(CAPITAL_GAINS_TAX_BRACKETS_FILE, 'r') as f:
        capital_gains_tax_brackets = json.load(f)

    with open(STANDARD_DEDUCTION, 'r') as f:
        standard_deduction = json.load(f)

    agi = regular_income + capital_gains
    combined_income = agi + social_security_benefits / 2
    social_security_taxable_amount = calculate_taxable_social_security_benefits(combined_income, social_security_thresholds[filing_status], social_security_benefits)
    taxable_income = max(0, regular_income + social_security_taxable_amount - standard_deduction[filing_status])
    tax_liability = calculate_tax_liability(taxable_income, income_tax_brackets[filing_status])
    capital_gains_tax_liability = calculate_long_term_capital_gains_tax_liability(taxable_income, capital_gains, capital_gains_tax_brackets[filing_status])
    total_taxes_owed = max(tax_liability + capital_gains_tax_liability,0)

    if regular_income + capital_gains + social_security_benefits > 0:
        effective_tax_rate = total_taxes_owed / (regular_income + capital_gains + social_security_benefits)
    else:
        effective_tax_rate = 0
    return (total_taxes_owed, effective_tax_rate)
