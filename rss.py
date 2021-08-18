import requests, cgi, cgitb
replacementurl = 'http://85.17.94.10/rinse/rinsefm/'
occurence = []
data = ''
try:
    data = str(requests.get('https://rinse.fm/search/hixxy/feed/rss2').text)
except:
    pass
dataor = data.split('<link>')
for i in dataor:
    if '/podcasts/' in i:
        occurence.append(i.split('</link>')[0])
for i in occurence:
    filename = i.split('/')[4].replace('h','H')
    data = data.replace(i , replacementurl + filename + '.mp3')
title = ''
for i in data.split('<channel>'):
    if '<title>' in i:
        title = i.split('<title>')[1].split('</title>')[0]
data = data.replace(title, 'Langwater.nl rss')
data = data.replace('London and Worldwide', 'balls lickin')

with open('/var/www/langwater/hixxy.rss', 'w') as file:
    file.write(data)
    file.close()
    