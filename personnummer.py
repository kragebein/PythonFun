#!/usr/bin/python3 
''' Genererer ekte Norske personnummer '''
import datetime, random, sys

class Persnr():
    def __init__(self):
        ''' Set rules '''
        if len(sys.argv) >= 2:
            #Input detected, treat as date
            year = int(sys.argv[1])
            month = int(sys.argv[2])
            day = int(sys.argv[3])
        else:
            year = 1970
            month = 1
            day = 1
        try:
            x = datetime.datetime(year, month, day)
        except ValueError:
            raise ValueError('Invalid date format. YEAR, MONTH, DAY')
        
        self.day = x.strftime("%d")
        self.month = x.strftime("%m")
        self.year = x.strftime("%y")
        self.longyear = year
        self.date = self.day+self.month+self.year
        self.individsifre = {
            '000-499': [1900,1999],
            '500-749': [1854,1899],
            '500-999': [2000,2039],
            '900-999': [1940,1999]
        }
        self.individtall = None
        self.indivitall1 = None
    def individ(self):
        ''' grabs a random individsiffer '''
        for x in self.individsifre:
            for _year in range(self.individsifre[x][0], self.individsifre[x][1]):
                if self.longyear == _year:
                    return (int(x.split('-')[0]), int(x.split('-')[1]))

    def calculate(self):
        ''' calculates controlchiphers using modulo ''' 
        
        i1, i2 = self.individ()
        rando = random.randint(i1, i2)
        self.individtall1 = rando
        ind = [i for i in map(int,str(rando))]
        self.individtall = ind
        day = [i for i in map(int,str(self.day))]
        month = [i for i in map(int,str(self.month))]
        year = [i for i in map(int,str(self.year))]
        k1 = 11 - ((3 * day[0] + 7 * day[1] + 6 * month[0] + 1 * month[1] + 8 * year[0] + 9 * year[1] + 4 * ind[0] +5 * ind[1] + 2 * ind[2]) % 11)
        k2 = 11 - ((5 * day[0] + 4 * day[1] + 3 * month[0] + 2 * month[1] + 7 * year[0] + 6 * year[1] + 5 * ind[0] +4 * ind[1] + 3 * ind[2] +2 * k1) % 11)
        if k1 > 10 or k2 > 10:
            # discard, calculate again!
            self.calculate()
        if k1 == 11:
            k1 = 0
        if k2 == 11:
            k2 = 0

        return (k1, k2)
    def get(self):
        '''sett sammen alt til et gyldig personnummer'''
        dato = self.date
        k1, k2 = self.calculate()
        if self.individtall[2] % 2 == 0:
            sex = 'Kvinne'
        else:
            sex = 'Mann'
        persnr = str(dato)+str(self.individtall1)+str(k1)+str(k2)
        return (sex,persnr)

def hent():
    x = Persnr()
    while True:
        try:
            data = x.get()
            if len(data[1]) == 11:
                print('{} - {}'.format(data[1], data[0]))
                return False
        except:
            pass

hent()


