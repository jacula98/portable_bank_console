import sqlite3
from rich import print
import os
import sys

"""
conn = sqlite3.connect('bank.db')
cur = conn.cursor()
cur.execute(f"DELETE FROM bank_history WHERE name = 'jacek';")
cur.execute(f"UPDATE bank_history 
                        SET 
                            main_category = 'food',
                            sub_category = 'fastfood',
                            value = '-20',
                            date = '2023-01-05'
                        WHERE id = '12'
        ;")
conn.commit()

cur.execute(f"DROP TABLE bank_history;")
conn.commit()
cur.execute(f"INSERT INTO bank_history(name, main_category, sub_category, value, date) VALUES ('Jacek', 'zabawa', '', -150, '');")
cur.execute(f"INSERT INTO bank_history(name, main_category, sub_category, value, date) VALUES ('Jacek', 'zabawa', '', -150, '');")
cur.execute(f"DROP TABLE users;")

cur.execute(f"DROP TABLE week_balance;")
"""


def startup():
    conn = create_connection('bank.db')
    if conn is not None:
        # create projects table
        configure_database(conn)
        return conn
    else:
        return "Error! cannot create the database connection or tables."

# clean true if u want to not clear screen or false if u dont want to clean
def bank_gui(input=None, user=None, clean=False):
    if input is None:
        if clean is True:
            os.system('cls')
        print("-----------------------------------")
        print("|                                 |")
        print("|   P O R T A B L E    B A N K    |")
        print("|                                 |")
        print("|                                 |")
        print("|   Options:                      |")
        print("|   1. Select user                |")
        print("|   2. Create user                |")
        print("|   3. Delete user                |")
        print("|                                 |")
        print("| Q to quit                       |")
        print("-----------------------------------")
    elif input == 1:
        if clean is True:
            os.system('cls')
        print("-----------------------------------")
        print("|                                 |")
        print("|   P O R T A B L E    B A N K    |")
        print("|                                 |")
        show_users()
        print("|                                 |")
        print("|   Options:                      |")
        print("|   B. Back to main page          |")
        print("|                                 |")
        print("|                                 |")
        print("| Q to quit                       |")
        print("-----------------------------------")
    elif input == 2:
        if clean is True:
            os.system('cls')
        print("-----------------------------------")
        print("|                                 |")
        print("|   P O R T A B L E    B A N K    |")
        print("|                                 |")
        print("|                                 |")
        print("|   Options:                      |")
        print("|   B. Back to main page          |")
        print("|                                 |")
        print("|   1. Add income/expense         |")
        print("|   2. Show history               |")
        print("|   3. Show statistics            |")
        print("|   4. Update/delete record       |")
        print("|                                 |")
        print("|   Or choose user below          |")
        print("|                                 |")
        print("| Q to quit                       |")
        print("-----------------------------------")
    elif input == 3:
        if clean is True:
            os.system('cls')
        print("-------------------------------------------------------------------------------")
        print("|                                                                             |")
        print("|                       P O R T A B L E    B A N K                            |")
        print("|                                                                             |")
        show_user_history(user)
        print("|                                                                             |")
        print("|   Options:                                                                  |")
        print("|   B. Back to main page                                                      |")
        print("|                                                                             |")
        print("| Q to quit                                                                   |")
        print("-------------------------------------------------------------------------------")
    elif input == 4:
        if clean is True:
            os.system('cls')
        print("-------------------------------------------------------------------------------")
        print("|                                                                             |")
        print("|                       P O R T A B L E    B A N K                            |")
        print("|                                                                             |")
        show_statistics(user)
        print("|                                                                             |")
        print("|   Options:                                                                  |")
        print("|   B. Back to main page                                                      |")
        print("|                                                                             |")
        print("| Q to quit                                                                   |")
        print("-------------------------------------------------------------------------------")
    elif input == 5:
        if clean is True:
            os.system('cls')
        print("-------------------------------------------------------------------------------")
        print("|                                                                             |")
        print("|                       P O R T A B L E    B A N K                            |")
        print("|                                                                             |")
        show_user_history(user, showID=True)
        print("|                                                                             |")
        print("|   Options:                                                                  |")
        print("|   1. Update record                                                          |")
        print("|   2. Delete record                                                          |")
        print("|                                                                             |")
        print("|   B. Back to main page                                                      |")
        print("|                                                                             |")
        print("| Q to quit                                                                   |")
        print("-------------------------------------------------------------------------------")
    else:
        print('Error in gui creation')


def show_statistics(user):
    conn = startup()
    print("-------------------------------------------------------------------------------")
    print("%-2s %-9s %-3s %s %3s %s %s %s %2s %s %s" %
          ("|", "Category", "|", "Avg. per week", "|", "Avg. per month", "|", "Last month", "|", "perc. diff.", "|"))
    try:
        cur = conn.cursor()
        cur.execute("""SELECT main_category, 
                        SUM(value) / (julianday((SELECT MAX(date) FROM bank_history)) - julianday((SELECT MIN(date) FROM bank_history))) * 7, 
                        SUM(value) / (julianday((SELECT MAX(date) FROM bank_history)) - julianday((SELECT MIN(date) FROM bank_history))) * 30,
                        (
                            SELECT SUM(value)
                            WHERE date >= date('now', 'start of month') AND date <= date('now')
                        )
                        FROM bank_history
                        GROUP BY main_category;""")
        rows = cur.fetchall()
        if len(rows) > 0:
            for row in rows:
                x = abs(row[3]) - abs(row[2])
                y = round((x / abs(row[2])) * 100, 1)
                print("%-2s %-9s %-7s %-11s %-5s %-10s %-5s %-7s %-4s %-8s %s" %
                ("|", row[0], "|", round(row[1], 1), "|", round(row[2], 1), "|", row[3], "|", y, "|"))
                       
                #else:
                #    print("%-2s %-9s %-7s %-11s %-5s %-10s %-6s %-6s %-6s %-6s %s" %
                #    ("|", row[0], "|", round(row[1], 1), "|", round(row[2], 1), "|", "-", "|", "-", "|"))
        print("-------------------------------------------------------------------------------")
    except Exception as e:
        print(e)


def show_user_history(user, showID=False):
    conn = startup()
    # update user balance
    updateStatus = update_balance(user)
    try:
        update_balance(user)
    except:
        return updateStatus

    try:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM bank_history WHERE name = '{user}' ORDER BY date;")
        rows = cur.fetchall()
    except Exception as e:
        print(e)

    with conn:
        if len(rows) > 0:
            print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
            if showID is False:
                print("-------------------------------------------------------------------------------")
                print("%s %10s %5s %12s %3s %14s %3s %12s %11s" %
                ("|", "Value", "|", "Category", "|", "Sub-category", "|", "Date", "|"))
                for row in rows:
                    # if date have hours it gonna split and show only yyyy-mm-dd, if not have hours, it gonna continue
                    date = str(row[5])
                    date = date.split(' ')
                    # sub category empty
                    if row[3] is None:
                        # value
                        if row[4] > 0:
                            value = str(row[4])
                            value = '[green]' + value + '[/green]'
                            print("%-7s %s %6s %12s %3s %12s %5s %15s %8s" %
                                ("|", value, "|", row[2], "|", '', "|", date[0], "|"))
                        elif row[4] < 1:
                            value = str(row[4])
                            value = '[red]' + value + '[/red]'
                            print("%-7s %s %6s %12s %3s %12s %5s %15s %8s" %
                                ("|", value, "|", row[2], "|", '', "|", date[0], "|"))
                    # sub category not empty
                    else:
                        # value
                        if row[4] > 0:
                            value = str(row[4])
                            value = '[green]' + value + '[/green]'
                            print("%-7s %s %7s %12s %3s %12s %5s %15s %8s" % (
                                "|", value, "|", row[2], "|", row[3], "|", date[0], "|"))
                        elif row[4] < 1:
                            value = str(row[4])
                            value = '[red]' + value + '[/red]'
                            if len(value) < 14:
                                print("%-7s %s %7s %12s %3s %12s %5s %15s %8s" % (
                                    "|", value, "|", row[2], "|", row[3], "|", date[0], "|"))
                            else:
                                print("%-7s %s %6s %12s %3s %12s %5s %15s %8s" % (
                                "|", value, "|", row[2], "|", row[3], "|", date[0], "|"))

            elif showID is True:
                print("%s %s %s %10s %5s %12s %3s %14s %3s %12s %11s" %
                ("|", "ID", "|", "Value", "|", "Category", "|", "Sub-category", "|", "Date", "|"))
                print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
                for row in rows:
                    # if date have hours it gonna split and show only yyyy-mm-dd, if not have hours, it gonna continue
                    date = str(row[5])
                    date = date.split(' ')
                    # sub category empty
                    if row[3] is None:
                        # value
                        if row[4] > 0:
                            value = str(row[4])
                            value = '[green]' + value + '[/green]'
                            print("%s %s %-7s %s %6s %12s %3s %12s %5s %15s %8s" %
                                ("|", row[0], "|", value, "|", row[2], "|", '', "|", date[0], "|"))
                        elif row[4] < 1:
                            value = str(row[4])
                            value = '[red]' + value + '[/red]'
                            print("%s %s %-7s %s %6s %12s %3s %12s %5s %15s %8s" %
                                ("|", row[0], "|", value, "|", row[2], "|", '', "|", date[0], "|"))
                    # sub category not empty
                    else:
                        # value
                        if row[4] > 0:
                            value = str(row[4])
                            value = '[green]' + value + '[/green]'
                            print("%s %s %-7s %s %7s %12s %3s %12s %5s %15s %8s" % 
                            ("|", row[0], "|", value, "|", row[2], "|", row[3], "|", date[0], "|"))
                        elif row[4] < 1:
                            value = str(row[4])
                            value = '[red]' + value + '[/red]'
                            if len(value) < 14:
                                print("%s %s %-7s %s %7s %12s %3s %12s %5s %15s %8s" % 
                                ("|", row[0], "|", value, "|", row[2], "|", row[3], "|", date[0], "|"))
                            else:
                                print("%s %s %-7s %s %6s %12s %3s %12s %5s %15s %8s" % 
                                ("|", row[0], "|", value, "|", row[2], "|", row[3], "|", date[0], "|"))
                print("-------------------------------------------------------------------------------")
        else:
            print(
                "-------------------------------------------------------------------------------")


def add_record(user):
    conn = startup()
    cur = conn.cursor()
    try:
        cur.execute(
            f"SELECT DISTINCT main_category FROM bank_history WHERE name = '{user}';")
        rows = cur.fetchall()
        os.system('cls')
        print("-------------------------------------------------------------------------------")
        print("|                                                                             |")
        print("|                       P O R T A B L E    B A N K                            |")
        print("|                                                                             |")
        print("|                         Categories used so far                              |")
        print("|                                                                             |")
        if len(rows) > 0:
            for row in rows:
                for category in row:
                    print("%-32s %-44s %s" % ("|", category, "|"))
        else:
            print("|                                                                             |")
            print('|                      No categories at this moment                           |')
        print("|                                                                             |")
        print("-------------------------------------------------------------------------------")
    except sqlite3.Error as error:
        print(error)

    mainCategory = input('Main category(REQUIRED): ')
    while len(mainCategory) < 1:
        mainCategory = input('Main category(REQUIRED): ')
    subCategory = input('Sub category(NOT REQUIRED): ')
    value = input('Amount: ')
    while len(value) < 1:
        value = input('Amount: ')
    date = input('Date(ex. 2023-01-09 or leave blank for current date): ')
    while len(date) < 10:
        date = input('Date(ex. 2023-01-09 or leave blank for current date) REMEMBER TO PUT 01-02 FOR DAYS AND MONTHS: ')
    # no date provided
    if len(date) < 1:
        # no subCategory provided
        if len(subCategory) < 1:
            try:
                cur.execute(f"""INSERT INTO bank_history(name, main_category, value) 
                                VALUES ('{user}', '{mainCategory}', '{value}')
                            ;""")
            except sqlite3.Error as error:
                return error
        else:
            try:
                cur.execute(f"""INSERT INTO bank_history(name, main_category, sub_category, value) 
                                VALUES ('{user}', '{mainCategory}', '{subCategory}', '{value}' )
                            ;""")
            except sqlite3.Error as error:
                return error
    # no subCategory provided
    elif len(subCategory) < 1:
        # also no date provided
        if len(date) < 1:
            try:
                cur.execute(f"""INSERT INTO bank_history(name, main_category, value) 
                                VALUES ('{user}', '{mainCategory}', '{value}')
                            ;""")
            except sqlite3.Error as error:
                return error
        else:
            try:
                cur.execute(f"""INSERT INTO bank_history(name, main_category, value, date) 
                                VALUES ('{user}', '{mainCategory}', '{value}', '{date}')
                            ;""")
            except sqlite3.Error as error:
                return error
    # all info provided
    else:
        try:
            cur.execute(f"""INSERT INTO bank_history(name, main_category, sub_category, value, date) 
                            VALUES ('{user}', '{mainCategory}', '{subCategory}', '{value}', '{date}')
                        ;""")
        except sqlite3.Error as error:
            return error
    conn.commit()
    updateStatus = update_balance(user)
    if updateStatus == 'succes':
        return 'succes'
    else:
        return updateStatus


def update_balance(user):
    conn = startup()
    cur = conn.cursor()
    try:
        cur.execute(f"""UPDATE users SET balance = (SELECT SUM(value) FROM bank_history WHERE users.name = '{user}')
                            ;""")
    except sqlite3.Error as error:
        return error
    conn.commit()
    return 'succes'


def update_record(id):
    conn = startup()
    cur = conn.cursor()
    mainCategory = input('New main category(REQUIRED): ')
    while len(mainCategory) < 1:
        mainCategory = input('New main category(REQUIRED): ')
    subCategory = input('New Sub category(NOT REQUIRED): ')
    value = input('New amount: ')
    while len(value) < 1:
        value = input('Amount: ')
    date = input('Date(ex. 2023-01-09 or leave blank for current date): ')
    while len(date) < 10:
        date = input('Date(ex. 2023-01-09 or leave blank for current date): ')
    try:
        cur.execute(f"""UPDATE bank_history 
                        SET 
                            main_category = '{mainCategory}',
                            sub_category = '{subCategory}',
                            value = '{value}',
                            date = '{date}'
                        WHERE id = '{id}'
        ;""")
        conn.commit()
        return 'succes'
    except sqlite3.Error as error:
        return error


def delete_record(id):
    conn = startup()
    cur = conn.cursor()
    try:
        cur.execute(f"DELETE FROM bank_history WHERE id = '{id}';")
        conn.commit()
    except sqlite3.Error as error:
        return error


def show_users():
    conn = startup()
    print("-----------------------------------")
    print("%s %10s %5s %12s %3s" % ("|", "User", "|", "Balance", "|"))
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    rows = cur.fetchall()
    with conn:
        if len(rows) > 0:
            print("- - - - - - - - - - - - - - - - - -")
            for row in rows:
                if row[2] > 0:
                    balance = str(row[2])
                    balance = '[green]' + balance + '[/green]'
                    print("%s %10s %5s %27s %3s" %
                          ("|", row[1], "|", balance, "|"))
                elif row[2] < 1:
                    balance = str(row[2])
                    balance = '[red]' + balance + '[/red]'
                    print("%s %10s %5s %23s %3s" %
                          ("|", row[1], "|", balance, "|"))
            print("-----------------------------------")
        else:
            print("-----------------------------------")


def select_user(user):
    if user == 'q':
        print('Quiting program...')
        sys.exit(0)
    elif user == 'b' or user == 'B':
        return 'mainpage'
    checked_user = check_user(user)
    if checked_user == 'found':
        return 'user_found'
    elif checked_user == 'not_found':
        return 'user_not_found'
    else:
        return 'Error durning checking user'


def check_user(user):
    conn = startup()
    cur = conn.cursor()
    cur.execute(f"SELECT name FROM users WHERE name = '{user}';")
    data = cur.fetchall()
    if len(data) == 0:
        return 'not_found'
    else:
        return 'found'


def configure_database(conn):
    try:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users (
						ID INTEGER PRIMARY KEY autoincrement,
                        name VARCHAR(255) NOT NULL UNIQUE,
                        balance INT DEFAULT 0
                                   ); """)
        c.execute("""CREATE TABLE IF NOT EXISTS bank_history (
                        id INTEGER PRIMARY KEY autoincrement,
                        name VARCHAR(255) NOT NULL,
                        main_category VARCHAR(255) NOT NULL,
                        sub_category VARCHAR(255),
                        value INT,
                        date DATE NOT NULL DEFAULT (strftime('%Y-%m-%d', 'now', 'localtime'))
                                    ); """)
        c.execute("""CREATE TABLE IF NOT EXISTS week_balance (
                        name VARCHAR(255) NOT NULL,
                        week INT,
                        week_balance INT
                                   ); """)
        conn.commit()
    except Exception as e:
        print(e)


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # print(f"Connecting to database: {db_file} is done")
    except Exception as e:
        print(e)

    return conn


def confirmation():
    response = input('Username: Are u sure? Y/N: ')
    if response == 'y' or response == 'Y':
        return True
    elif response == 'n' or response == 'N':
        return False
    else:
        return confirmation()


def create_person(name):
    conn = startup()
    try:
        cur = conn.cursor()
        cur.execute(f"""INSERT INTO users(name)
                        VALUES ('{name}');""")
        conn.commit()
        return 'succes'
    except sqlite3.Error as error:
        return error


def delete_person(name):
    conn = startup()
    try:
        cur = conn.cursor()
        cur.execute(f"DELETE FROM users WHERE name='{name}'")
        conn.commit()
        print(f"Deleting person '{name}' is done")
        return 'succes'
    except sqlite3.Error as error:
        return error
