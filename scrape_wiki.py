import requests as rq
from bs4 import BeautifulSoup
from datetime import date, datetime


url = 'https://lista.mercadolivre.com.br/celular'
resp = rq.get(url)
soup = BeautifulSoup(resp.text, 'html.parser')
infos = soup.find_all('div', class_ = "item__info-container highlighted")

dic_precos = {"nome":[], "preço":[]}

for info in infos:
	nome = info.find('span')
	preco_fraction = info.find('span', class_ = "price__fraction")
	preco_decimals = info.find('span', class_ = "price__decimals")
	if preco_decimals == None:
		preco_final = preco_fraction.text + "," + "00"
		print(nome.text + " - " + preco_final)
	else:
		preco_final = preco_fraction.text + "," + preco_decimals.text
		print(nome.text + " - " + preco_final)
	preco_format = preco_final.replace('.', '').replace(',', '.')
	
	dic_precos['nome'].append(nome.text)
	dic_precos['preço'].append(float(preco_format))

preco_maximo = max(dic_precos['preço'])
nome_maximo = dic_precos['nome'][dic_precos['preço'].index(preco_maximo)]

preco_minimo = min(dic_precos['preço'])
nome_minimo = dic_precos['nome'][dic_precos['preço'].index(preco_minimo)]

media = sum(dic_precos['preço']) / len(dic_precos['preço'])


html = f'''
<!DOCTYPE html>
<html>
<head>
	<title>Celular mais barato da primeira página do Mercado livre</title>
</head>
<body>
	<h1>O Celular mais barato</h1>
	<p>
		No dia {datetime.date} o celular mais barato era {nome_minimo}, com valor {preco_minimo}.
	</p>
</body>
</html>
		'''

with open('index.html', 'w+') as index:
	index.write(html)
