# Homomorphic-Encryption-for-Loan-Eligibility-Assessment
We have established a hypothetical financial institution named "Bank of Kuber," where "Kuber" symbolizes wealth in Indian mythology.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Screenshot](#screenshot)

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
2. Create a virtual environment and activate it:
  ```bash
  python -m venv venv
  source venv/bin/activate
  ```
4. Install the required packages:
  ```bash
  pip install -r requirements.txt
  ```
5. Run the Flask application
  ```bash
  python loanClient.py
  python loanServer.py
  ```
