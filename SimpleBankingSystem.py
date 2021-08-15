# Write your code here
import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')
conn.commit()

while True:
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    customer_input = int(input(">"))
    print()
    if customer_input not in [0, 1, 2]:
        print("Choose a correct option")
        print()
    elif customer_input == 1:
        account_number = random.randint(100000000, 999999999)
        partial_card = "400000" + str(account_number)
        card_list = list(partial_card)
        numbers_in_card = []
        for card_digits in card_list:
            numbers_in_card.append(int(card_digits))
        d = 0
        for c in numbers_in_card:
            if d % 2 == 0:
                numbers_in_card[d] = numbers_in_card[d] * 2
            d += 1
        n = 0
        for k in numbers_in_card:
            if k > 9:
                numbers_in_card[n] = k - 9
            n += 1
        total_num = 0
        for ele in range(0, len(numbers_in_card)):
            total_num = total_num + numbers_in_card[ele]
        control_num = total_num
        x = 0
        while True:
            if (control_num + x) % 10 == 0:
                card_number = partial_card + str(x)
                break
            x += 1
        PIN = str(random.randint(1000, 9999))
        cur.execute(f'INSERT INTO card (number, pin) VALUES ({card_number}, {PIN});')
        conn.commit()
        print("Your card has been created")
        print("Your card number:")
        cur.execute('SELECT (number) FROM (card) ORDER BY (id) DESC;')
        print(str(cur.fetchone()).strip("(',')"))
        print("Your card PIN:")
        cur.execute('SELECT (pin) FROM (card) ORDER BY (id) DESC;')
        print(str(cur.fetchone()).strip("(',')"))
        print()
    elif customer_input == 2:
        print("Enter your card number:")
        customer_card = int(input(">"))
        print("Enter your PIN:")
        customer_pin = int(input(">"))
        print()
        y = list(str(customer_card))
        last_digit = y[-1]
        y.pop(-1)
        numbers = []
        for i in y:
            numbers.append(int(i))
        z = 0
        for x in numbers:
            if z % 2 == 0:
                numbers[z] = numbers[z] * 2
            z += 1
        y = 0
        for b in numbers:
            if b > 9:
                numbers[y] = b - 9
            y += 1
        numbers.append(int(last_digit))
        total = 0
        for element in range(0, len(numbers)):
            total = total + numbers[element]
        x_pin = str(customer_pin)
        db_pin = cur.execute(f'SELECT pin FROM card WHERE number = ({str(customer_card)});')
        y_pin = str(cur.fetchone()).strip("(',')")
        if (total % 10 != 0) and x_pin != y_pin:
            print("Wrong card number and PIN!")
            print()
        if (total % 10 != 0) or x_pin != y_pin:
            print("Wrong card number or PIN!")
            print()
        else:
            print("You have successfully logged in!")
            print()
            while True:
                chosen_option = []
                print("1. Balance")
                print("2. Add Income")
                print("3. Do Transfer")
                print("4. Close Account")
                print("5. Log out")
                print("0. Exit")
                customer_option = int(input(">"))
                print()
                if customer_input not in [0, 1, 2]:
                    print("Choose a correct option")
                    print()
                elif customer_option == 1:
                    chosen_option.append(customer_option)
                    cur.execute(f'SELECT (balance) FROM (card) WHERE number = {str(customer_card)};')
                    b = str(cur.fetchone()).strip("(',')")
                    print(f"Balance: {b}")
                    print()
                elif customer_option == 2:
                    print("Enter income:")
                    customer_income = int(input(">"))
                    cur.execute(f'UPDATE card SET balance = (balance + {customer_income}) WHERE number = ({str(customer_card)});')
                    conn.commit()
                    print("Income was added!")
                    print()
                elif customer_option == 3:
                    print("Transfer")
                    print("Enter your card number:")
                    customer_card_luhn = int(input(">"))
                    cur.execute(f'SELECT number FROM card WHERE number = {str(customer_card_luhn)};')
                    e = cur.fetchone()
                    cur.execute(f'SELECT number FROM card WHERE number = {str(customer_card)};')
                    v = str(cur.fetchone()).strip("(',')")
                    h = list(str(customer_card_luhn))
                    last_digit_2 = h[-1]
                    h.pop(-1)
                    numbers_2 = []
                    for i in h:
                        numbers_2.append(int(i))
                    k = 0
                    for x in numbers_2:
                        if k % 2 == 0:
                            numbers_2[k] = numbers_2[k] * 2
                        k += 1
                    g = 0
                    for c in numbers_2:
                        if c > 9:
                            numbers_2[g] = c - 9
                        g += 1
                    numbers_2.append(int(last_digit_2))
                    card_total = 0
                    for elem in range(0, len(numbers_2)):
                        card_total = card_total + numbers_2[elem]
                    if str(customer_card_luhn) == v:
                        print("You can't transfer money to the same account!")
                        print()
                    elif card_total % 10 != 0:
                        print("Probably you made a mistake in the card number. Please try again!")
                        print()
                    elif e is None:
                        print("Such a card does not exist.")
                        print()
                    else:
                        print("Enter how much money you want to transfer:")
                        customer_transfer = int(input(">"))
                        cur.execute(f'SELECT (balance) FROM (card) WHERE number = {str(customer_card)};')
                        customer_acct_balance = int(str(cur.fetchone()).strip("(',')"))
                        if customer_transfer > customer_acct_balance:
                            print("Not enough money!")
                            print()
                        elif customer_transfer <= customer_acct_balance:
                            cur.execute(f'UPDATE card SET balance = (balance - {customer_transfer}) WHERE number = ({str(customer_card)});')
                            conn.commit()
                            cur.execute(f'UPDATE card SET balance = (balance + {customer_transfer}) WHERE number = ({str(customer_card_luhn)});')
                            conn.commit()
                            print("Success!")
                            print()
                elif customer_option == 4:
                    chosen_option.append(customer_option)
                    cur.execute(f'DELETE FROM card WHERE number = {str(customer_card)};')
                    conn.commit()
                    print("The account has been closed!")
                    print()
                    break
                elif customer_option == 5:
                    chosen_option.append(customer_option)
                    print("You have successfully logged out!")
                    print()
                    break
                elif customer_option == 0:
                    chosen_option.append(customer_option)
                    break
            if chosen_option[-1] == 0:
                conn.close()
                print("Bye!")
                break
    elif customer_input == 0:
        conn.close()
        print("Bye!")
        break
