# Banking System — Python

A command-line banking application developed in Python, featuring customer and financial advisor accounts, basic banking operations, loan eligibility calculations, and customer-advisor messaging.

## Overview

This project implements a simplified banking system with two user roles: **Customers** and **Financial Advisors**. Each role has access to specific features, with data stored locally in text files.

The application is designed as an educational project to practice Python programming, object-oriented design, file handling, authentication, and financial calculations.

## Features

### Customer

- **Account balance:** Check the current account balance.
- **Money transfers:** Transfer money to another customer's account using their RIB.
- **Withdrawals:** Withdraw money while checking available funds.
- **Deposits:** Add money to the account balance.
- **Personal details:** Update username, password, and monthly net salary.
- **Loan eligibility:** Calculate the maximum additional monthly loan payment based on a 33% debt-to-income threshold.
- **Messaging:** Send messages to the assigned financial advisor.

### Financial Advisor

- **Customer management:** List customers assigned to the advisor.
- **Account consultation:** Check a customer's account balance.
- **Loan assessment:** Calculate a customer's loan eligibility.
- **Customer creation:** Add new customers to the system.
- **Customer deletion:** Delete customers assigned to the advisor.
- **Messaging:** Read messages sent by assigned customers.

### General Features

- Separate customer and advisor authentication.
- Maximum of three login attempts per session.
- Input validation for amounts and text fields.
- Prevention of withdrawals and transfers exceeding available funds.
- Prevention of transfers to the sender's own account.
- Persistent local data storage using text files.
- Automatic creation of data files with demonstration data on first launch.

## Technologies

- **Language:** Python 3.10+
- **Data structures:** Classes and dataclasses
- **Data storage:** Plain-text files (CSV-style format)
- **Interface:** Command-line interface (CLI)
- **Dependencies:** Python standard library only

## Project Structure

```text
banking-system/
├── banking.py       # Main application and banking operations
├── customers.txt    # Customer account data (generated automatically)
├── advisors.txt     # Financial advisor credentials (generated automatically)
├── messages.txt     # Customer-advisor messages (generated automatically)
└── README.md        # Project documentation
```

The three data files are created automatically when the application starts if they do not already exist.

## Installation and Usage

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

Replace `YOUR-USERNAME` and `YOUR-REPOSITORY` with your GitHub username and repository name.

### 2. Run the application

Make sure Python 3.10 or later is installed, then execute:

```bash
python3 banking.py
```

### 3. Select a user role

When prompted, enter:

- `1` for Customer
- `2` for Financial Advisor

Then enter the corresponding username and password.

## Demonstration Accounts

The application initializes sample accounts on its first run.

### Customers

| Username | Password |
|---|---|
| `AnnaB` | `tWp54@` |
| `Kate78` | `Zpt#$5` |
| `JohnD` | `jD2#5!` |
| `MaryS` | `mS#3rS` |
| `AlexT` | `aT!2zs` |

### Financial Advisors

| Username | Password |
|---|---|
| `advisor1` | `pass1` |
| `advisor2` | `pass2` |

These credentials are provided exclusively for local demonstration and testing.

## Financial Logic

### Loan Eligibility

The maximum additional monthly loan payment is calculated using a debt-to-income threshold of 33%:

```python
eligible_payment = max(
    0.0,
    0.33 * net_monthly_salary - existing_monthly_loan_payments
)
```

If the result is zero, the application considers the customer ineligible for an additional monthly loan payment.

This calculation is a simplified educational model and does not represent an actual bank's lending decision.

## Data Storage

The application uses three local text files:

- `customers.txt`: RIB, advisor ID, username, password, date of birth, net monthly salary, existing monthly loan payments, and account balance.
- `advisors.txt`: Advisor ID, username, and password.
- `messages.txt`: Advisor ID, customer RIB, and message content.

Changes to customer account data are saved to the corresponding file, while messages are appended to the message file.

**Important:** These files contain demonstration data and are not suitable for storing real financial or personal information.

## Security and Limitations

This project is a simplified banking simulation, not a production-ready banking application.

Current limitations include:

- Passwords are stored in plain text.
- Data is stored in local text files without encryption.
- Authentication does not use a secure password-hashing mechanism.
- There is no database, transaction history, or audit log.
- The application does not implement real banking APIs or payment processing.
- Loan eligibility is based on a simplified calculation.

The application should only be used with fictional data in a local development environment.

## Future Improvements

Potential extensions include:

- Secure password hashing and stronger authentication.
- Database integration using SQLite or PostgreSQL.
- Transaction history and account statements.
- Improved input validation and error handling.
- Automated unit and integration tests.
- A graphical user interface or web application.
- More comprehensive loan assessment criteria.

## License

No license has been specified yet. Add a `LICENSE` file if you intend to distribute or reuse this project under specific terms.

---

*An educational Python project exploring banking operations, object-oriented programming, data persistence, and financial calculations.*
