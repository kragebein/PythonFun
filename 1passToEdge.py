''' Move usernames and passwords from 1password export file to Edge compatible csv'''
import json
data = None
onepass='C:/Users/stian/Desktop/pw/export.data'
csvfile = 'C:/Users/stian/Desktop/pw/import.csv'
delimiter = ','
with open(onepass, 'r', encoding="utf-8") as brrt:
    data = json.loads(brrt.read())
count = 0
csv = f'name{delimiter}url{delimiter}username{delimiter}password\n'
for x in data['accounts'][0]['vaults'][0]['items']:
    item = x['item']['overview']['title']
    username = None
    password = None
    url = None
    title = None
    if len(x['item']['details']['loginFields']) <= 1:
        # Skip entry created with app.
        continue        
    username = x['item']['details']['loginFields'][0]['value']
    password = x['item']['details']['loginFields'][1]['value']
    url = x['item']['overview']['urls'][0]['url']
    title = x['item']['overview']['title']
    csv = csv + f'{title}{delimiter}{url}{delimiter}{username}{delimiter}{password}\n'
    count += 1
    if delimiter in password:
        print(f'[WARNING] {item}s password contains the delimiter. This could break importing')
    if delimiter in username:
         print(f'[WARNING] {item}s username contains the delimiter. This could break importing')
    if delimiter in url:
         print(f'[WARNING] {item}s url contains the delimiter. This could break importing')
    if delimiter in item:
        print(f'[WARNING] {item}s name contains the delimiter. This could break importing')

with open(csvfile, 'w', encoding="utf-8") as export:
    export.write(csv)
print(f'Exported {count} usernames and passwords from {onepass} and made csv here: {csvfile}')
