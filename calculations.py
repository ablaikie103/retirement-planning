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

def calculate_tax_liability(taxable_income, tax_brackets):
    """
    Calculates the tax liability based on taxable income and tax brackets.
    Args:
    taxable_income (float): The taxable income.
    tax_brackets (list): A list of tuples representing the tax brackets. Each tuple contains three values: 
    the lower limit of the bracket, the upper limit of the bracket, and the tax rate for that bracket.
    Returns:
    float: The tax liability.
    """
    tax_liability = 0
    for bracket in tax_brackets:
        if taxable_income > bracket[0]:
            taxable_amount = min(taxable_income, bracket[1]) - bracket[0]
            tax_liability += taxable_amount * bracket[2]
        else:
            break
    return tax_liability


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
    income_tax_brackets = {
        "single": [
            (0, 11000, 0.1),
            (11000, 44725, 0.12),
            (44725, 86375, 0.22),
            (86375, 164925, 0.24),
            (164925, 209425, 0.32),
            (209425, 523600, 0.35),
            (523600, float('inf'), 0.37)
        ],
        "married": [
            (0, 19900, 0.1),
            (19900, 81050, 0.12),
            (81050, 172750, 0.22),
            (172750, 329850, 0.24),
            (329850, 418850, 0.32),
            (418850, 628300, 0.35),
            (628300, float('inf'), 0.37)
        ]
    }

    social_security_thresholds = {
            'single': {'base_amount': 25000, 'phaseout': 9000},
            'married': {'base_amount': 32000, 'phaseout': 12000}
        }
    
    capital_gains_tax_brackets = {
        "single": [
            {"lower_limit": 0, "upper_limit": 40000, "tax_rate": 0},
            {"lower_limit": 40000, "upper_limit": 441450, "tax_rate": 0.15},
            {"lower_limit": 441450, "upper_limit": float('inf'), "tax_rate": 0.20}
        ],
        "married": [
            {"lower_limit": 0, "upper_limit": 80000, "tax_rate": 0},
            {"lower_limit": 80000, "upper_limit": 496600, "tax_rate": 0.15},
            {"lower_limit": 496600, "upper_limit": float('inf'), "tax_rate": 0.20}
        ]
    }

    agi = regular_income + capital_gains
    combined_income = agi + social_security_benefits / 2
    social_security_taxable_amount = calculate_taxable_social_security_benefits(combined_income, social_security_thresholds[filing_status], social_security_benefits)
    standard_deduction = 25550 if filing_status == "married" else 12775
    taxable_income = max(0, regular_income + social_security_taxable_amount - standard_deduction)
    tax_liability = calculate_tax_liability(taxable_income, income_tax_brackets[filing_status])
    capital_gains_tax_liability = calculate_long_term_capital_gains_tax_liability(taxable_income, capital_gains, capital_gains_tax_brackets[filing_status])
    total_taxes_owed = tax_liability + capital_gains_tax_liability
    effective_tax_rate = total_taxes_owed / (regular_income + capital_gains + social_security_benefits)

    return (total_taxes_owed, effective_tax_rate)


