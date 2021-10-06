#!/usr/bin/python3.6
''' generate passwords and avoids combinations that hold both username and users name in the password '''
import string, random
username = 'stilan'
name = 'Stian Langvann'

def check(password, char):
    for x in password:
        if password[:-1] + char in username or password[:-1] + char in name:
            return True
        return False

def genpass(special_chars=True, length=20):
    char = string.ascii_letters + string.digits
    char = char + '@$!%?&¤#/()[]' if special_chars == True else char
    password = ''
    while len(password) <= length:
        try: 
            x = char[random.randint(0, len(char))]
            if check(password, x):
                x = char[random.randint(0, len(char))]
            password = password + x
        except:
            pass
    print(password)
def gen(chars, len, amount):
    c = 0
    while c <= amount:
        genpass(special_chars=chars, length=len)
        c += 1
# gen(special characters on/off, number of characters, how many passwords to generate)

gen(1, 25, 50)
 