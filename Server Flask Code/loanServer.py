from flask import Flask, request, Response, json
import numpy as np
from Pyfhel import Pyfhel, PyCtxt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///creditScore.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.app_context().push()

class CreditScore(db.Model):
    pan = db.Column(db.String(10), primary_key=True)
    cibil_score = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f"PAN: {self.pan} | CIBIL Score:{self.cibil_score}"

# Create DB with sample values
def init_db():
    with app.app_context():
        db.create_all()

    exists = CreditScore.query.filter_by(pan='CAAPR4080A').first()
    if not exists:
        cibil1 = CreditScore(pan='CAAPR4080A', cibil_score=590)
        db.session.add(cibil1)
        db.session.commit()
    exists = CreditScore.query.filter_by(pan='CAAPR4080B').first()
    if not exists:
        cibil2 = CreditScore(pan='CAAPR4080B', cibil_score=680)
        db.session.add(cibil2)
        db.session.commit()
    exists = CreditScore.query.filter_by(pan='CAAPR4080C').first()
    if not exists:
        cibil3 = CreditScore(pan='CAAPR4080C', cibil_score=750)
        db.session.add(cibil3)
        db.session.commit()

@app.route("/fhe_repayment_capacity", methods=['POST'])
def fhe_repayment_capacity():
    request_data = request.get_json()

    HE_server = Pyfhel()
    HE_server.from_bytes_context(request_data['context'].encode('cp437'))
    HE_server.from_bytes_public_key(request_data['pk'].encode('cp437'))
    HE_server.from_bytes_relin_key(request_data['rlk'].encode('cp437'))
    HE_server.from_bytes_rotate_key(request_data['rtk'].encode('cp437'))
    monthly_income_cx = PyCtxt(pyfhel=HE_server, bytestring=request_data['monthly_income_cx'].encode('cp437'))
    monthly_debt_cx = PyCtxt(pyfhel=HE_server, bytestring=request_data['monthly_debt_cx'].encode('cp437'))
    print(f"[Server] received HE_server={HE_server} \t monthly_income_cx={monthly_income_cx} \t monthly_debt_cx={monthly_debt_cx}")

    creditScoreObj = CreditScore.query.filter_by(pan=request_data['pan']).first()
    print("[Server] Credit Score: ", creditScoreObj)
    credit_score = creditScoreObj.cibil_score

    # Calculate monthly repayment capacity

    repayment_capacity_cx = cx_calculate_repayment_capacity(HE_server, monthly_income_cx, monthly_debt_cx, credit_score)

    print(f"[Server] Monthly Repayment Capacity in Ciphertext: {repayment_capacity_cx}")

    return Response(response=json.dumps({"repayment_capacity_cx": repayment_capacity_cx.to_bytes().decode('cp437')}), status=200, mimetype='application/json')

def calculate_repayment_capacity(monthly_income, monthly_debt, credit_score):
    # Define criteria and factors for credit score adjustments
    credit_score_criteria = {
        (300, 579): 0.1,  # Adjust for poor credit
        (580, 669): 0.3,  # Adjust for fair credit
        (670, 739): 0.4,  # No adjustment for good credit
        (740, 799): 0.5,  # Adjust for very good credit
        (800, 850): 0.6,  # Adjust for excellent credit
    }

    # Find the applicable credit score adjustment factor
    credit_score_factor = 0.5
    for (lower, upper), factor in credit_score_criteria.items():
        if lower <= credit_score < upper:
            credit_score_factor = factor
            break

    # Calculate Loan Eligibility
    repayment_capacity = (monthly_income - (2*monthly_debt)) * credit_score_factor

    return repayment_capacity

def cx_calculate_repayment_capacity(HE_server, monthly_income_cx, monthly_debt_cx, credit_score):
    # Define criteria and factors for credit score adjustments
    credit_score_criteria = {
        (300, 579): 0.1,  # Adjust for poor credit
        (580, 669): 0.3,  # Adjust for fair credit
        (670, 739): 0.4,  # No adjustment for good credit
        (740, 799): 0.5,  # Adjust for very good credit
        (800, 850): 0.6,  # Adjust for excellent credit
    }

    # Find the applicable credit score adjustment factor
    credit_score_factor = 0.5
    for (lower, upper), factor in credit_score_criteria.items():
        if lower <= credit_score < upper:
            credit_score_factor = factor
            break

    ptxt_credit_score_factor = HE_server.encodeFrac(np.array([credit_score_factor]))

    twice_monthly_debt = HE_server.encodeFrac(np.array([2.0])) * monthly_debt_cx

    income_minus_twice_monthly_debt = monthly_income_cx - twice_monthly_debt

    # Calculate Loan Eligibility
    repayment_capacity = income_minus_twice_monthly_debt * ptxt_credit_score_factor

    return repayment_capacity

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
