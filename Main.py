#! /usr/bin/python3
import argparse
import sqlite3
from faker import Faker

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

TD = Faker("en_GB")  # this can be set to other languages see docs for more info


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
    """
    entity: C, U, PA, PR, A
    """
    entity = entity.upper()
    if entity == "C":
        print("Selecting customers")
        select_customers()
    elif entity == "U":
        print("Selecting users")
        select_users()
    elif entity == "PA":
        print("Selecting parts")
        select_parts()
    elif entity == "PR":
        print("Selecting products")
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

        print_title("All info selected")
    else:
        raise ValueError(f"Unsupported entity for read: {entity}")


def run_write(entity: str, multi: bool, count: int):
    """
    entity: C, U, PA, PR, A
    multi: whether to create multiple records
    count: number of records when multi is True
    """
    entity = entity.upper()

    # Ensure DB exists
    dbinit()

    if entity == "A":
        # For "All", we just use count for all multi-create calls when multi=True.
        if multi:
            print(f"Creating {count} of each: users, parts, products (clothes)")
            multi_create_product_clothes(count)
            multi_create_users(count)
            multi_create_parts(count)
        else:
            print("Creating single records for users/parts/products (clothes)")
            create_product_clothes()
            create_user()
            create_part()
        return

    if entity == "C":
        if multi:
            print(f"Creating {count} customers")
            multi_create_customers(count)
        else:
            print("Creating single customer")
            create_customer()

    elif entity == "U":
        if multi:
            print(f"Creating {count} users")
            multi_create_users(count)
        else:
            print("Creating single user")
            create_user()

    elif entity == "PA":
        if multi:
            print(f"Creating {count} parts")
            multi_create_parts(count)
        else:
            print("Creating single part")
            create_part()

    elif entity == "PR":
        # Here I assume you mainly want clothes; you can extend this to shoes/bedding/towels
        if multi:
            print(f"Creating {count} product clothes")
            multi_create_product_clothes(count)
        else:
            print("Creating single product clothes")
            create_product_clothes()
    else:
        raise ValueError(f"Unsupported entity for write: {entity}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Test data generator (non-interactive mode for ECS)"
    )
    parser.add_argument(
        "--mode",
        "-m",
        choices=["R", "W"],
        required=False,
        default="W",  # default: WRITE mode
        help="R = READ, W = WRITE (default: W)",
    )
    parser.add_argument(
        "--entity",
        "-e",
        choices=["C", "U", "PA", "PR", "A"],
        required=False,
        default="A",  # default: All entities
        help="C=Customers, U=Users, PA=Parts, PR=Products, A=All (default: A)",
    )
    parser.add_argument(
        "--multi",
        "-M",
        action="store_true",
        help="For WRITE mode: create multiple records (default: False)",
    )
    parser.add_argument(
        "--count",
        "-c",
        type=int,
        default=10,  # default number of records when multi is used
        help="Number of records to create when using --multi (default: 10)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    mode = args.mode.upper()
    entity = args.entity.upper()

    if mode == "R":
        print(f"Running READ for entity {entity}")
        run_read(entity)
    elif mode == "W":
        print(
            f"Running WRITE for entity {entity} "
            f"(multi={args.multi}, count={args.count})"
        )
        run_write(entity, args.multi, args.count)
    else:
        raise ValueError(f"Unsupported mode: {mode}")


if __name__ == "__main__":
    main()
