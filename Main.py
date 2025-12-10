#! /usr/bin/python3
import argparse
import sqlite3
from faker import Faker
from flask import Flask, request   # NEW: Flask for web mode

from Users import (
    create_user,
    multi_create_users,
    select_users,
)
from Customers import (
    create_customer,
    multi_create_customers,
    select_customers,
)
from Parts import (
    create_part,
    multi_create_parts,
    select_parts,
)
from Products import (
    create_product_clothes,
    create_product_shoes,
    create_product_bedding,
    create_product_towel,
    multi_create_product_clothes,
    multi_create_product_towels,
    multi_create_product_bedding,
    multi_create_product_shoes,
    select_products,
)

TD = Faker("en_GB")


def dbinit():
    conn = sqlite3.connect("TestData.db")
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS USERS ("
        "UID INTEGER PRIMARY KEY, "
        "First_Name TEXT, "
        "Last_Name TEXT, "
        "Birthdate TEXT DEFAULT '01-01-1899',"
        "Contact_Number TEXT,"
        "Email TEXT, "
        "Password TEXT, "
        "Job_Title TEXT DEFAULT 'Worker',"
        "StartDate TEXT DEFAULT '01-01-1899');"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS CUSTOMERS ("
        "CID INTEGER PRIMARY KEY, "
        "First_Name TEXT, "
        "Last_Name TEXT, "
        "Birthdate TEXT DEFAULT '01-01-1899', "
        "Address TEXT DEFAULT '123 WISHING LANE', "
        "Contact_Number TEXT, "
        "Email TEXT, "
        "Password TEXT);"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS INVOICEHEADER ("
        "INVHEADID INTEGER PRIMARY KEY, "
        "Customer_AccountNo TEXT, "
        "Customer_Name TEXT, "
        "Customer_Address TEXT, "
        "Contact_Number TEXT,"
        "Email TEXT);"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS INVOICELINES ("
        "IVNLINE INTEGER PRIMARY KEY,  "
        "First_Name TEXT, "
        "Last_Name TEXT, "
        "Contact_Number TEXT);"
    )

    conn.commit()
    conn.close()
    print("Database initialised")


def print_title(title: str):
    print("################")
    print(title)
    print("################")


def run_read(entity: str):
    entity = entity.upper()
    if entity == "C":
        select_customers()
    elif entity == "U":
        select_users()
    elif entity == "PA":
        select_parts()
    elif entity == "PR":
        select_products()
    elif entity == "A":
        dbinit()
        print_title("Customers")
        select_customers()
        print_title("Users")
        select_users()
        print_title("Parts")
        select_parts()
        print_title("Products")
        select_products()
    else:
        raise ValueError(f"Unsupported entity for read: {entity}")


def run_write(entity: str, multi: bool, count: int):
    entity = entity.upper()

    dbinit()

    if entity == "A":
        if multi:
            multi_create_product_clothes(count)
            multi_create_users(count)
            multi_create_parts(count)
        else:
            create_product_clothes()
            create_user()
            create_part()
        return

    if entity == "C":
        if multi:
            multi_create_customers(count)
        else:
            create_customer()

    elif entity == "U":
        if multi:
            multi_create_users(count)
        else:
            create_user()

    elif entity == "PA":
        if multi:
            multi_create_parts(count)
        else:
            create_part()

    elif entity == "PR":
        if multi:
            multi_create_product_clothes(count)
        else:
            create_product_clothes()
    else:
        raise ValueError(f"Unsupported entity for write: {entity}")


# ------------------------------------------------------
# NEW: Minimal Web UI / API
# ------------------------------------------------------
def run_web():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return (
            "<h2>TestDataGen Web Interface</h2>"
            "<p>Use /generate or /read</p>"
            "<p>Example: /generate?entity=A&multi=true&count=10</p>"
        )

    @app.route("/health")
    def health():
        return "OK", 200

    @app.route("/generate")
    def generate():
        entity = request.args.get("entity", "A")
        multi_str = request.args.get("multi", "false")
        count = int(request.args.get("count", "10"))
        multi = multi_str.lower() in ("true", "1", "yes", "y")

        run_write(entity, multi, count)
        return f"Generated data: entity={entity}, multi={multi}, count={count}"

    @app.route("/read")
    def read():
        entity = request.args.get("entity", "A")
        run_read(entity)
        return f"Read entity={entity}. Check logs."

    print("Starting Web Server at http://localhost:5000 ...")
    app.run(host="0.0.0.0", port=5000)


# ------------------------------------------------------
# Argument Parser (supports normal + web mode)
# ------------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(description="Test Data Generator")

    parser.add_argument("--web", action="store_true",
                        help="Start web interface on port 5000")

    parser.add_argument("--mode", "-m", choices=["R", "W"],
                        required=False, default="W")

    parser.add_argument("--entity", "-e",
                        choices=["C", "U", "PA, PR", "A"],
                        required=False, default="A")

    parser.add_argument("--multi", "-M", action="store_true")
    parser.add_argument("--count", "-c", type=int, default=10)

    return parser.parse_args()


def main():
    args = parse_args()

    if args.web:
        run_web()
        return

    mode = args.mode.upper()
    entity = args.entity.upper()

    if mode == "R":
        run_read(entity)
    elif mode == "W":
        run_write(entity, args.multi, args.count)
    else:
        raise ValueError(f"Unsupported mode: {mode}")


if __name__ == "__main__":
    main()
