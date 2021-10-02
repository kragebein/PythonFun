''' Matrix rain attempt '''
import random as r 
import time
import os
import string

symbols = [i for i in string.digits]
for i in (0, 15):
    if i / 3:
        symbols.insert(i, ' ')
line = []
counter = 0

for i in range(118):
    x = r.randint(0, len(symbols) -1)
    line.append(symbols[x])
    counter += 1
k = 0
while True:
    
    if counter % 5 == 0:
        r_symbols = [r.randint(0, 117) for x in range (10)]

        for i in r_symbols:
            line[i] = symbols[r.randint(0, len(symbols) -1)]
    print(' '.join(line))
    counter += 1 
    time.sleep(0.01)
    k += 1