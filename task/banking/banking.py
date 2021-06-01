# Write your code here
import random
import sqlite3


class Account:
    account = {}

    def __init__(self):
        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS card(id INTEGER PRIMARY KEY AUTOINCREMENT,'
                    'number TEXT,'
                    'pin TEXT,'
                    'balance INTEGER DEFAULT 0)')
        conn.commit()

    def find_details(self, number):
        con = sqlite3.connect('card.s3db')
        curs = con.cursor()
        try:
            curs.execute(f'SELECT * FROM card WHERE number = {number}')
            detail = curs.fetchone()
        except:
            return None
        return detail

    @staticmethod
    def verify_luhns(card_no, verify):
        luhns_algo = []  # Implementing Luhn's Algo
        for i in range(15):
            if i % 2 == 0:
                temp = card_no[i] * 2  # Multiplication and subtraction at same time
                if temp >= 10:
                    temp -= 9
                luhns_algo.append(temp)
            else:
                luhns_algo.append(card_no[i])

        check_sum = 10 - sum(luhns_algo) % 10
        if check_sum == 10:
            check_sum = 0
        card_number = 0
        for i in card_no:  # Generating Card Number
            card_number = card_number * 10 + i
        card_number = card_number * 10 + check_sum
        if verify == 'generate':
            return card_number
        elif verify == 'verify':
            if card_no[-1] == check_sum:
                return True
            else:
                return False

    def gen_card_details(self):
        card_no = [4, 0, 0, 0, 0, 0]  # Institution ID

        for i in range(9):  # Generating Account Number
            temp = random.randint(0, 9)
            card_no.append(temp)

        card_number = self.verify_luhns(card_no, 'generate')

        pin = ''  # Generating PIN
        for i in range(4):
            pin += str(random.randint(0, 9))

        details = self.find_details(card_number)
        if details == -1:
            self.gen_card_details()
        return card_number, pin

    def create_account(self):
        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()
        card_no, pin = self.gen_card_details()
        cur.execute(f'INSERT INTO CARD(number, pin) '
                    f'VALUES({str(card_no)}, {str(pin)})')
        conn.commit()
        conn.close()
        print(f'''Your card number:\n{card_no}''')
        print(f'''Your card PIN:\n{pin}\n''')

    def log_account(self):
        card = input('Enter your card number:\n')
        pin = input('Enter your PIN:\n')
        details = self.find_details(card)
        if details is None:
            print('Wrong card number or PIN!')
            return 0
        else:
            try:
                if details[2] == pin:
                    print('You have successfully logged in!')
                    x = self.login_actions(details[1])
                    return x
                else:
                    raise Exception
            except:
                print('Wrong card number or PIN!')
            return 0

    def login_actions(self, number):
        con = sqlite3.connect('card.s3db')
        curs = con.cursor()
        while True:
            print('1. Balance')
            print('2. Add income')
            print('3. Do transfer')
            print('4. Close account')
            print('5. Log out')
            print('0. Exit')
            ch = int(input())
            detail = self.find_details(number)
            if ch == 0:
                return -1
            elif ch == 1:
                print(f'Balance: {detail[3]}')
            elif ch == 2:
                income = int(input('Enter income:\n'))
                curs.execute(f'UPDATE card SET balance = balance + {income} WHERE number = {number}')
                con.commit()
                print('Income was added!')
            elif ch == 3:
                print('Transfer')
                t_card = input('Enter card number:\n')
                t_card_ls = list(map(int, list(t_card)))
                verify = self.verify_luhns(t_card_ls, 'verify')
                if verify:
                    t_detail = self.find_details(t_card)
                    if t_detail is None:
                        print('Such a card does not exist.')
                    else:
                        print('Enter how much money you want to transfer:\n')
                        t_amount = int(input())
                        if t_amount > detail[3]:
                            print('Not enough money!')
                        else:
                            curs.execute(f'UPDATE card SET balance = balance + {t_amount} WHERE number = {t_card}')
                            curs.execute(f'UPDATE card SET balance = balance - {t_amount} WHERE number = {number}')
                            con.commit()
                            print('Success!')
                else:
                    print('Probably you made a mistake in the card number. Please try again!')
            elif ch == 4:
                curs.execute(f'DELETE FROM card WHERE number = {detail[1]}')
                con.commit()
            elif ch == 5:
                print("You have successfully logged out!")
                break

if __name__ == '__main__':
    acc = Account()
    while True:
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')
        inp = int(input())

        if inp == 0:
            print('Bye!')
            break
        elif inp == 1:
            acc.create_account()
        elif inp == 2:
            x = acc.log_account()
            if x == -1:
                break
