from calculations import calculate_federal_taxes
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

if __name__ == '__main__':
    app.run(debug=True)