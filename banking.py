#!/usr/bin/env python3
"""Banking system : version Python du programme C (clients et conseillers).

Fichiers de données (créés avec des données d'exemple s'ils n'existent pas) :
  customers.txt : RIB,advisorID,username,password,dob,salary,loanPayments,balance
  advisors.txt  : advisorID,username,password
  messages.txt  : advisorID,customerRIB,message
"""
import os
from dataclasses import dataclass

CUSTOMERS_FILE = "customers.txt"
ADVISORS_FILE = "advisors.txt"
MESSAGES_FILE = "messages.txt"
DEBT_RATIO = 0.33  # taux d'endettement maximal utilisé pour l'éligibilité au prêt
MAX_LOGIN_ATTEMPTS = 3

SEED_CUSTOMERS = """\
14707080701234567890139,12345,AnnaB,tWp54@,20/10/1995,2500,500.6,7890.25
14707080701234567890156,12345,Kate78,Zpt#$5,10/05/1978,4000,0,45233.99
14707080701234567890157,20003,JohnD,jD2#5!,15/03/1985,3200,200,15000.50
14707080701234567890158,20003,MaryS,mS#3rS,22/06/1990,2800,100,6200.75
14707080701234567890159,12345,AlexT,aT!2zs,30/12/1975,5000,1000,95000.99
"""
SEED_ADVISORS = """\
12345,advisor1,pass1
20003,advisor2,pass2
"""


# --------------------------------------------------------------------------- #
# Modèles
# --------------------------------------------------------------------------- #
@dataclass
class Customer:
    rib: str
    advisor_id: str
    username: str
    password: str
    dob: str
    net_monthly_salary: float
    total_monthly_loan_payments: float
    current_account_balance: float

    def to_line(self) -> str:
        return ",".join([
            self.rib, self.advisor_id, self.username, self.password, self.dob,
            f"{self.net_monthly_salary:g}",
            f"{self.total_monthly_loan_payments:g}",
            f"{self.current_account_balance:.2f}",
        ])

    @classmethod
    def from_line(cls, line: str) -> "Customer":
        p = line.strip().split(",")
        return cls(p[0], p[1], p[2], p[3], p[4], float(p[5]), float(p[6]), float(p[7]))


@dataclass
class Advisor:
    advisor_id: str
    username: str
    password: str


# --------------------------------------------------------------------------- #
# Fichiers
# --------------------------------------------------------------------------- #
def ensure_data_files() -> None:
    for path, seed in ((CUSTOMERS_FILE, SEED_CUSTOMERS), (ADVISORS_FILE, SEED_ADVISORS)):
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(seed)
    if not os.path.exists(MESSAGES_FILE):
        open(MESSAGES_FILE, "w", encoding="utf-8").close()


def load_customers() -> list[Customer]:
    with open(CUSTOMERS_FILE, encoding="utf-8") as f:
        return [Customer.from_line(l) for l in f if l.strip()]


def save_customers(customers: list[Customer]) -> None:
    with open(CUSTOMERS_FILE, "w", encoding="utf-8") as f:
        for c in customers:
            f.write(c.to_line() + "\n")


def load_advisors() -> list[Advisor]:
    with open(ADVISORS_FILE, encoding="utf-8") as f:
        return [Advisor(*l.strip().split(",")[:3]) for l in f if l.strip()]


def append_message(advisor_id: str, rib: str, message: str) -> None:
    with open(MESSAGES_FILE, "a", encoding="utf-8") as f:
        f.write(f"{advisor_id},{rib},{message}\n")


# --------------------------------------------------------------------------- #
# Saisie sécurisée
# --------------------------------------------------------------------------- #
def ask_text(prompt: str) -> str:
    """Texte non vide, sans virgule (le séparateur du format de fichier)."""
    while True:
        value = input(prompt).strip()
        if value and "," not in value:
            return value
        print("Invalid input (empty or contains a comma).")


def ask_amount(prompt: str, allow_zero: bool = False) -> float | None:
    try:
        amount = round(float(input(prompt).replace(",", ".")), 2)
    except ValueError:
        print("Invalid amount.")
        return None
    if amount < 0 or (amount == 0 and not allow_zero):
        print("Amount must be positive.")
        return None
    return amount


def ask_choice(prompt: str) -> int:
    try:
        return int(input(prompt))
    except ValueError:
        return -1


# --------------------------------------------------------------------------- #
# Authentification
# --------------------------------------------------------------------------- #
def login_customer(customers, username, password) -> int:
    for i, c in enumerate(customers):
        if c.username == username and c.password == password:
            return i
    return -1


def login_advisor(advisors, username, password) -> int:
    for i, a in enumerate(advisors):
        if a.username == username and a.password == password:
            return i
    return -1


# --------------------------------------------------------------------------- #
# Opérations client
# --------------------------------------------------------------------------- #
def check_balance(c: Customer) -> None:
    print(f"Current balance for {c.username}: {c.current_account_balance:.2f}")


def deposit(c: Customer, amount: float) -> None:
    c.current_account_balance += amount
    print(f"Deposit successful! New balance: {c.current_account_balance:.2f}")


def withdraw(c: Customer, amount: float) -> bool:
    if amount > c.current_account_balance:
        print("Insufficient funds.")
        return False
    c.current_account_balance -= amount
    print(f"Withdrawal successful! New balance: {c.current_account_balance:.2f}")
    return True


def transfer_money(customers, sender_index: int, recipient_rib: str, amount: float) -> bool:
    sender = customers[sender_index]
    recipient = next((c for c in customers if c.rib == recipient_rib), None)
    if recipient is None:
        print("Recipient not found.")
        return False
    if recipient is sender:
        print("You cannot transfer money to your own account.")
        return False
    if amount > sender.current_account_balance:
        print("Insufficient funds.")
        return False
    sender.current_account_balance -= amount
    recipient.current_account_balance += amount
    print(f"Transfer successful! New balance: {sender.current_account_balance:.2f}")
    return True


def loan_eligibility(c: Customer) -> float:
    """Mensualité maximale supplémentaire : 33 % du salaire net - mensualités en cours."""
    return max(0.0, DEBT_RATIO * c.net_monthly_salary - c.total_monthly_loan_payments)


def print_loan_eligibility(c: Customer) -> None:
    limit = loan_eligibility(c)
    if limit > 0:
        print(f"Eligible for a loan up to: {limit:.2f}")
    else:
        print("Not eligible for a loan.")


def update_personal_details(customers, c: Customer) -> bool:
    print("what do you want to change ? :")
    print("1. Username\n2. password\n3. Monthly salary")
    choice = ask_choice("enter choice : ")
    if choice == 1:
        new = ask_text("Enter new username: ")
        if any(o.username == new and o is not c for o in customers):
            print("Username already taken.")
            return False
        c.username = new
    elif choice == 2:
        c.password = ask_text("Enter new password: ")
    elif choice == 3:
        salary = ask_amount("Enter new monthly salary: ")
        if salary is None:
            return False
        c.net_monthly_salary = salary
    else:
        print("Invalid choice.")
        return False
    print("Details updated successfully.")
    return True


def send_message(c: Customer) -> None:
    message = input("Enter your message: ").strip().replace("\n", " ")
    if not message:
        print("Empty message.")
        return
    append_message(c.advisor_id, c.rib, message)
    print("Message sent.")


# --------------------------------------------------------------------------- #
# Opérations conseiller
# --------------------------------------------------------------------------- #
def read_messages(advisor_id: str) -> None:
    count = 0
    with open(MESSAGES_FILE, encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split(",", 2)
            if len(parts) == 3 and parts[0] == advisor_id:
                print(f"Message from {parts[1]}: {parts[2]}")
                count += 1
    if count == 0:
        print("You don't have any message...")


def find_by_rib(customers, rib: str) -> Customer | None:
    return next((c for c in customers if c.rib == rib), None)


def add_customer(customers, advisor: Advisor) -> bool:
    rib = ask_text("Enter RIB: ")
    if find_by_rib(customers, rib):
        print("A customer with this RIB already exists.")
        return False
    username = ask_text("Enter username: ")
    if any(c.username == username for c in customers):
        print("Username already taken.")
        return False
    password = ask_text("Enter password: ")
    dob = ask_text("Enter date of birth (DD/MM/YYYY): ")
    salary = ask_amount("Enter net monthly salary: ", allow_zero=True)
    loans = ask_amount("Enter total monthly loan payments: ", allow_zero=True)
    balance = ask_amount("Enter initial balance: ", allow_zero=True)
    if None in (salary, loans, balance):
        return False
    customers.append(Customer(rib, advisor.advisor_id, username, password, dob,
                              salary, loans, balance))
    print("Customer added successfully.")
    return True


def delete_customer(customers, advisor: Advisor) -> bool:
    rib = ask_text("Enter RIB of the customer to delete: ")
    target = find_by_rib(customers, rib)
    if target is None or target.advisor_id != advisor.advisor_id:
        print("Customer not found among your customers.")
        return False
    if input(f"Delete {target.username}? (y/n): ").strip().lower() != "y":
        print("Cancelled.")
        return False
    customers.remove(target)
    print("Customer deleted.")
    return True


def list_customers(customers, advisor: Advisor) -> None:
    mine = [c for c in customers if c.advisor_id == advisor.advisor_id]
    if not mine:
        print("You have no customers.")
    for c in mine:
        print(f"{c.rib}  {c.username:<10} balance: {c.current_account_balance:.2f}")


# --------------------------------------------------------------------------- #
# Menus
# --------------------------------------------------------------------------- #
CUSTOMER_MENU = """\
1. Check Balance
2. Transfer Money
3. Withdraw
4. Deposit
5. Update Personal Details
6. Loan Eligibility
7. Send Message
8. Log Out"""

ADVISOR_MENU = """\
1. List my customers
2. Check a customer's balance
3. Loan eligibility of a customer
4. Add customer
5. Delete customer
6. Read messages
7. Log Out"""


def customer_session(customers, index: int) -> None:
    c = customers[index]
    while True:
        print(CUSTOMER_MENU)
        choice = ask_choice("Enter choice: ")
        changed = False
        if choice == 1:
            check_balance(c)
        elif choice == 2:
            rib = ask_text("Enter recipient RIB: ")
            amount = ask_amount("Enter amount: ")
            if amount is not None:
                changed = transfer_money(customers, index, rib, amount)
        elif choice == 3:
            amount = ask_amount("Enter amount to withdraw: ")
            if amount is not None:
                changed = withdraw(c, amount)
        elif choice == 4:
            amount = ask_amount("Enter amount to deposit: ")
            if amount is not None:
                deposit(c, amount)
                changed = True
        elif choice == 5:
            changed = update_personal_details(customers, c)
        elif choice == 6:
            print_loan_eligibility(c)
        elif choice == 7:
            send_message(c)
        elif choice == 8:
            print("Logging out...")
            return
        else:
            print("Invalid choice.")
        if changed:
            save_customers(customers)


def advisor_session(customers, advisor: Advisor) -> None:
    while True:
        print(ADVISOR_MENU)
        choice = ask_choice("Enter choice: ")
        changed = False
        if choice == 1:
            list_customers(customers, advisor)
        elif choice in (2, 3):
            c = find_by_rib(customers, ask_text("Enter customer RIB: "))
            if c is None or c.advisor_id != advisor.advisor_id:
                print("Customer not found among your customers.")
            elif choice == 2:
                check_balance(c)
            else:
                print_loan_eligibility(c)
        elif choice == 4:
            changed = add_customer(customers, advisor)
        elif choice == 5:
            changed = delete_customer(customers, advisor)
        elif choice == 6:
            read_messages(advisor.advisor_id)
        elif choice == 7:
            print("Logging out...")
            return
        else:
            print("Invalid choice.")
        if changed:
            save_customers(customers)


# --------------------------------------------------------------------------- #
# Programme principal
# --------------------------------------------------------------------------- #
def main() -> None:
    ensure_data_files()
    customers = load_customers()
    advisors = load_advisors()

    role = ask_choice("Enter role (1 for Customer, 2 for Advisor): ")
    if role not in (1, 2):
        print("Invalid role.")
        return

    for _ in range(MAX_LOGIN_ATTEMPTS):
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        if role == 1:
            idx = login_customer(customers, username, password)
        else:
            idx = login_advisor(advisors, username, password)
        if idx >= 0:
            print("Login successful!")
            if role == 1:
                customer_session(customers, idx)
            else:
                advisor_session(customers, advisors[idx])
            return
        print("Invalid credentials.")
    print("Too many failed attempts.")


if __name__ == "__main__":
    main()
