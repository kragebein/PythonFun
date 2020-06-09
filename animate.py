import string, random, time
def animate(data):
    
    pool = [i for i in string.ascii_letters+string.digits+string.punctuation+' ']
    poolsize = len(pool)
    text = []
    for i in data:
        text.append(i)
    length = len(text)
    cipher = []
    newchar = []
    def flip(location):
        while True:
            try:
                randchar = pool[random.randint(0, poolsize)]
                return text[location] if randchar == text[location] else randchar
            except:
                pass
    for i in range(0, length):
        cipher.append(flip(i))
    output = ''.join(cipher)
    print('\r{}'.format(output), end='', flush=True)
    lockedchars = []
    newchar = cipher
    while True:
        for i in range(0, length):
            if newchar[i] == text[i]:
                pass # Lock character in place   
            else:
                data = flip(i)
                newchar[i] = data
                time.sleep(0.01)
                print('\r{}'.format(''.join(newchar)), end='', flush=True)
        if newchar == text:
            #When every character is locked, stop.
            print('')
            return False
animate('What the fuck is going on man')