from flask import Flask, render_template, request
import locale

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/fhe_home_loan_eligibility", methods=['GET', 'POST'])
def fhe_loan_eligibility():
    initial_loan_amount = 0
    monthly_repayment_capacity = 0

    oldPan = ""
    oldIncomeValue = ""
    oldDebtValue = ""
    oldTenureValue = ""
    oldInterestValue = ""
    incomeValue = ""
    debtValue = ""

    if request.method == 'POST':
        oldPan = request.form['pan']
        oldIncomeValue = request.form['incomeValue']
        oldDebtValue = request.form['debtValue']
        oldTenureValue = request.form['tenureValue']
        oldInterestValue = request.form['interestValue']

        pan = oldPan
        incomeValue = float(oldIncomeValue.replace(",", ""))
        debtValue = float(oldDebtValue.replace(",", ""))
        tenureValue = int(oldTenureValue)
        interestValue = float(oldInterestValue)

        print("[Client] PAN ID: ", pan)
        print("[Client] Income: ", incomeValue)
        print("[Client] Debt: ", debtValue)
        print("[Client] Tenure: ", tenureValue)
        print("[Client] Interest: ", interestValue)

        USE_REAL_SERVER: bool = True

        # %%
        # 1. Setup Client
        # --------------------------
        import numpy as np
        from Pyfhel import Pyfhel, PyCtxt
        if USE_REAL_SERVER:
            try:
                import requests
            except ImportError:
                print("This demo requires the `requests` python module (install with pip). Exiting.")
                exit(0)

        # Generate Pyfhel session
        print(f"[Client] Initializing Pyfhel session and data...")
        HE_client = Pyfhel(context_params={'scheme':'ckks', 'n':2**13, 'scale':2**30, 'qi_sizes':[30]*5}) # n/2 values can be encoded in a single cipher text.
        HE_client.keyGen()             # Generates both a public and a private key
        HE_client.relinKeyGen()
        HE_client.rotateKeyGen()

        # Generate and encrypt data
        monthly_income = np.array([incomeValue])
        c_monthly_income = HE_client.encrypt(monthly_income)

        monthly_debt = np.array([debtValue])
        c_monthly_debt = HE_client.encrypt(monthly_debt)

        # Serializing data and public context information
        s_context = HE_client.to_bytes_context()    # Note that, to operate, the ciphertexts/plaintexts must be built with the same context.
        s_public_key = HE_client.to_bytes_public_key()
        s_relin_key = HE_client.to_bytes_relin_key()
        s_rotate_key = HE_client.to_bytes_rotate_key()
        monthly_income_cx = c_monthly_income.to_bytes()
        monthly_debt_cx = c_monthly_debt.to_bytes()

        print(f"[Client] sending HE_client={HE_client}")

        # %%
        # 2. Launch a request to the server
        # ----------------------------------------
        #  We map the bytes into strings
        if(USE_REAL_SERVER):

            r = requests.post('http://127.0.0.1:5000/fhe_repayment_capacity',
                json={
                    'context': s_context.decode('cp437'),
                    'pk': s_public_key.decode('cp437'),
                    'rlk':s_relin_key.decode('cp437'),
                    'rtk':s_rotate_key.decode('cp437'),
                    'monthly_income_cx': monthly_income_cx.decode('cp437'),
                    'monthly_debt_cx': monthly_debt_cx.decode('cp437'),
                    'pan': pan,
                })

            c_emi = PyCtxt(pyfhel=HE_client, bytestring=r.json().get('repayment_capacity_cx').encode('cp437'))

            # %%
            # 3. Process Response
            # --------------------------
            # Decrypting result
            res = HE_client.decryptFrac(c_emi)
            monthly_repayment_capacity = int(round(res[0],0))
            print("[Client] Decrypted Repayment Capacity: ", monthly_repayment_capacity)

            annual_interest_rate = interestValue / 100  # 8.5% annual interest rate
            tenure = 12 * tenureValue  # Loan tenure in months

            # Calculate the initial loan amount

            initial_loan_amount = calculate_loan_principal(monthly_repayment_capacity, annual_interest_rate, tenure)

            print(f"[Client] Initial Loan Amount: ${round(initial_loan_amount,0)}")

    locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
    formatted_initial_loan_amount = locale.currency(int(round(initial_loan_amount,0)), grouping=True)
    formatted_initial_loan_amount = formatted_initial_loan_amount.replace(locale.localeconv()['currency_symbol'], '')

    formatted_monthly_repayment_capacity = locale.currency(int(round(monthly_repayment_capacity,0)), grouping=True)
    formatted_monthly_repayment_capacity = formatted_monthly_repayment_capacity.replace(locale.localeconv()['currency_symbol'], '')

    # Default values when the page loads
    if request.method == 'GET':
        return render_template('eligibility_calculator.html', initial_loan_amount=formatted_initial_loan_amount, monthly_repayment_capacity=formatted_monthly_repayment_capacity,
                               incomeValue='25,000', incomeRange='25000', debtValue='0', debtRange='0', tenureValue='30', interestValue='8.5')

    return render_template('eligibility_calculator.html', initial_loan_amount=formatted_initial_loan_amount, monthly_repayment_capacity=formatted_monthly_repayment_capacity,
                           pan=oldPan, incomeValue=oldIncomeValue, incomeRange=int(incomeValue), debtValue=oldDebtValue, debtRange=int(debtValue), tenureValue=oldTenureValue, interestValue=oldInterestValue)

def calculate_loan_principal(emi, annual_interest_rate, tenure):
    # Convert annual interest rate to monthly interest rate
    monthly_interest_rate = annual_interest_rate / 12.0

    # Calculate principal loan amount (P)
    loan_principal = emi / (monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** (-tenure)))

    return loan_principal

@app.route("/about_us")
def about_us():
    return render_template('about_us.html')

if __name__ == "__main__":
    app.run(debug=True, port=8000)
