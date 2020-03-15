import requests
from bs4 import BeautifulSoup
import texttable

page = requests.get('https://www.ojogodobicho.com/deu_no_poste.htm')

soup = BeautifulSoup(page.text, 'html.parser')

results = soup.find('table', attrs={'class':'twelve'})
results_itens = results.find_all('td')
titulo = results.find('caption').contents[0]
contents = [x.contents[0] for x in results_itens]
chunks = [contents[x:x+3] for x in range(0, len(contents), 3)]
final = texttable.Texttable()
final.add_rows([['','PTM','PT']], header=True)
for row in chunks:
    final.add_row(row)
print(titulo)
print(final.draw())
'''
for item in results_itens:
    content = item.contents[0]
    print(content)
    '''
