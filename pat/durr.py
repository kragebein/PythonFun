#!/usr/bin/python3.8
import requests
from bs4 import BeautifulSoup



search = 'https://mrplant.se/en/product-search/'
url = 'https://mrplant.se/'
input = ''
with open('input.txt', 'r') as brrt:
    input = brrt.read().split('\n')
    brrt.close()

print('parsing {} items\n'.format(len(input)))

def get(id):
    x = requests.get(search + id)
    if x.status_code == 200:
        return x.text
    else:
        return False

def parse(i):
    x = requests.get(url + i)
    if x.status_code != 200:
        return False
    soup = BeautifulSoup(x.text, 'html.parser')
    title = soup.find('title')
    #print('Parsing {}'.format(title.string.strip()))
    data = soup.find('div', {'id': 'productInfo'})
    text = data.text.split('\n')
    text = list(filter(None, text))
    name = text[0].strip()
    ind = 0
    color = None
    size = None
    #Process data. To add more entries, add an elif, look for 'blah' in x:
    # add the variable above this comment as blah = None, and blah = 'Whatever' + text[ind+1]
    # also add it to the important output below
    for x in text:
        if 'Colour' in x:
            color = text[ind+1].strip()
        elif 'Height' in x:
            size = 'Height' + text[ind+1]
        elif 'Length' in x:
            size = 'Length' + text[ind+1]
        elif 'Diameter' in x:
            size = 'Diameter' + text[ind+1]
        ind += 1
    
    output = '{};{};{}'.format(name, color, size) #important
    
    print(output)

    with open('output.txt', 'a') as brrt:
        brrt.write(output + '\n')
        brrt.close()
    
for item in input:
    data = get(item)
    soup = BeautifulSoup(data, 'html.parser')
    links = soup.find_all('a', href=True)
    for link in links:
        if item in link.get('href') and 'item' in link.get('href'):
            parse(link.get('href'))
        
    
    


