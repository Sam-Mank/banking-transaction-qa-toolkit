# Banking Transaction Reconciliation Tool

## Project Overview

This project is a Python-based QA tool designed to compare expected banking transactions against processed transactions.

It identifies discrepancies that could indicate processing errors, data quality issues or unexpected transaction activity.

The project uses fictional transaction data for demonstration and learning purposes.

## Key Features

- Compares expected and processed transaction records.
- Identifies missing transactions.
- Detects duplicate transaction IDs.
- Checks transaction amount mismatches.
- Checks transaction status mismatches.
- Identifies unexpected transactions.
- Validates mandatory fields and transaction amounts.
- Produces a CSV reconciliation report.
- Includes automated unit tests using Python's unittest framework.

## Technologies Used

- Python
- CSV data processing
- Decimal arithmetic for financial values
- Unit testing
- Git version control

## Project Structure

- `reconcile.py` – Main reconciliation application.
- `test_reconcile.py` – Automated test cases.
- `input_transactions.csv` – Expected transaction data.
- `processed_transactions.csv` – Processed transaction data.
- `reconciliation_report.csv` – Generated reconciliation results.

## How to Run

1. Activate the Python virtual environment.
2. Run the reconciliation script:

   `python reconcile.py`

3. Review the results displayed in the terminal.
4. Open `reconciliation_report.csv` to inspect the findings.

## Testing

Automated tests can be run using:

`python -m unittest -v`

The test suite covers successful reconciliation and a range of transaction discrepancies and invalid data scenarios.

## Learning Objectives

This project demonstrates practical QA skills including data validation, defect detection, automated testing, financial data reconciliation and version control.

All transaction data is fictional and created for educational purposes.