from calculations import calculate_federal_taxes
from models import run_monte_carlo_simulation
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate_taxes', methods=['POST'])
def calculate_taxes():
    regular_income = float(request.form['regular_income'])
    capital_gains = float(request.form['capital_gains'])
    social_security_benefits = float(request.form['social_security_benefits'])
    filing_status = request.form['filing_status']
     
    taxes_owed, effective_rate = calculate_federal_taxes(regular_income, capital_gains, social_security_benefits, filing_status)
    
    taxes_owed_formatted = '${:,.2f}'.format(taxes_owed)
    effective_rate_formatted = '{:.2%}'.format(effective_rate)

    return render_template('result.html', taxes_owed=taxes_owed_formatted, effective_rate=effective_rate_formatted)

@app.route('/simulate_retirement', methods=['POST'])
def simulate_retirement():
    amount_saved = float(request.form['amount_saved'])
    desired_spending = float(request.form['desired_spending'])
    contributions = float(request.form['contributions'])
     
    pass_percentage, fail_percentage = run_monte_carlo_simulation(amount_saved, desired_spending, contributions, 30, 30, 0.8, 200)
    pass_percentage_formatted = '{:.1%}'.format(pass_percentage/100)

    return render_template('sim_result.html', pass_percentage=pass_percentage_formatted)


if __name__ == '__main__':
    app.run(debug=True)