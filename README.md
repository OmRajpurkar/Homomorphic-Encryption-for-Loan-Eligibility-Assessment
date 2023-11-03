# Homomorphic-Encryption-for-Loan-Eligibility-Assessment
We have established a hypothetical financial institution named "Bank of Kuber," where "Kuber" symbolizes wealth in Indian mythology.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Screenshots](#screenshots)
- [References](#references)

## Features
- **Client Web App:**
  - User Interface: The client web app provides an intuitive interface for users to input financial data, including income, debt, tenure, and interest rate.
  - Homomorphic Encryption: Sensitive user data, such as income and debt, is encrypted using homomorphic encryption techniques, ensuring the confidentiality and security of the data.
  - Data Transmission: The client web app securely sends a request to the server web app to calculate the monthly repayment capacity based on the user's input.

- **Server Web App:**
  - Flask API: The server web app is built using Flask and serves as an API to accept POST requests from the client.
  - Credit Score Retrieval: It retrieves the user's credit score from the database to aid in the loan eligibility assessment.
  - Computation: Utilizing a proprietary formula, the server web app calculates the user's monthly repayment capacity. Importantly, this computation is performed on homomorphically encrypted income and debt data, preserving data privacy.
  - Result Delivery: The server web app returns the computed result, which is also encrypted, to the client web app, ensuring end-to-end data security and privacy throughout the process.

## Installation
1. Clone the repository:
  ```bash
  git clone https://github.com/yourusername/your-repo.git
   ```
3. Create a virtual environment and activate it:
  ```bash
  python -m venv venv
  venv/Scripts/activate.bat
  ```
3. Install the required packages:
  ```bash
  pip install -r requirements.txt
  ```
4. Run the Flask application
  ```bash
    python loanClient.py
    python loanServer.py
  ```

## Screenshots

**Home Page**

<img src="https://github.com/OmRajpurkar/Homomorphic-Encryption-for-Loan-Eligibility-Assessment/blob/main/Screenshots/Home_page.png" alt="alt text" width="850" height="450">

**Loan Eligibility Calculator**

<img src="https://github.com/OmRajpurkar/Homomorphic-Encryption-for-Loan-Eligibility-Assessment/blob/main/Screenshots/Loan_eligibility.png" alt="alt text" width="850" height="450">

**About Us**

<img src="https://github.com/OmRajpurkar/Homomorphic-Encryption-for-Loan-Eligibility-Assessment/blob/main/Screenshots/About_us.png" alt="alt text" width="850" height="450">

## References

- <a href="https://dl.acm.org/doi/abs/10.1145/1536414.1536440">Fully homomorphic encryption using ideal lattices</a>
- <a href="https://link.springer.com/chapter/10.1007/978-3-319-70694-8_15">Homomorphic Encryption for Arithmetic of Approximate Number</a>
- <a href="https://link.springer.com/chapter/10.1007/978-3-319-78381-9_14">Bootstrapping for Approximate Homomorphic Encryption</a>
- <a href="https://wvvw.easychair.org/publications/download/HWfT">Homomorphic encryption and data security in the cloud</a>
- <a href="https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=78ce2ec2f2b3f965fbcc8	a71bdb2d11c2b099b17">Alice and Bob in Cipherspace</a>
- <a href="https://hal.science/hal-03506798/">Faster homomorphic comparison operations for BGV and BFV</a>
- <a href="https://link.springer.com/chapter/10.1007/978-3-030-12612-4_5">An Improved RNS Variant of the BFV Homomorphic Encryption Scheme</a>
