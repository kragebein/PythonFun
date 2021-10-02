''' Get your daily horoscope here '''
from datetime import datetime
import requests, json, random
class stjerntegn():
    def __init__(self):
        self.total = 365
        self.stjerentegn = {
            'Aries': ['80', '110'],
            'Taurus': ['111', '141'],
            'Gemini': ['142', '172'],
            'Cancer': ['173', '203'],
            'Leo': ['204', '235'],
            'Virgo': ['236', '266'],
            'Libra': ['267', '296'],
            'Scorpio': ['297', '326'],
            'Sagittarius': ['627', '355'],
            'Capricornus': ['356', '20'],
            'Aquarius': ['21', '48'],
            'Pisces': ['49', '79']
        }
        #run self.
        self._input()
    def _input(self):
        date_format = "%d/%m/%Y"
        data = input('Enter your date of birth in form 01/03 (first of march)\n# ')
        dato = data.split('/')
        day = dato[0]
        month = dato[1]
        a = datetime.strptime('{}/{}/2020'.format(day, month), date_format)
        date = int(a.strftime('%j')) - 1
        date = str(date)
        _range = []
        for i in self.stjerentegn:
            for y in range(int(self.stjerentegn[i][0]), int(self.stjerentegn[i][1])):
                _range.append(y)
            if int(date) in _range:
                print('You were born in the mighty zodiac sign of {}'.format(i.upper()))
                x = requests.get('https://www.horoscopes-and-astrology.com/json')
                data = json.loads(x.text)
                print(data['dailyhoroscope'][i].split('<a href=')[0])
                break
            else:
                _range = []

stjerntegn()