from bs4 import BeautifulSoup
import requests
import csv
import sys


###################################

S = requests.Session()

URL = "https://wikis.uni-paderborn.de/graffiti/api.php"

PARAMS = {
    "action": "query",
    "meta": "tokens",
    "type": "login",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS)
# print(R.text)
DATA = R.json()

LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

# print(LOGIN_TOKEN)


PARAMS_1 = {
    'action':"login",
    'lgname':"",
    'lgpassword':"",
    'lgtoken':LOGIN_TOKEN,
    'format':"json"
}
URL2 = "https://wikis.uni-paderborn.de/graffiti/api.php"

R = S.post(URL2, data=PARAMS_1)

DATA = R

# print(DATA.text)
######################################

url = sys.argv[1]
url = 'https://wikis.uni-paderborn.de/graffiti/api.php?action=parse&page=Informationen_zu_den_Namen_(Pseudonymen)&format=json'
# url = 'https://wikis.uni-paderborn.de/graffiti/Informationen_zu_den_Namen_(Pseudonymen)'
response=S.get(url)

# print(response.content)

tableNames = {
	"0": "Übersicht Crews",
	"1": "Übersicht Sprayer",
	"2": "Übersicht Zahlen",
	"3": "Übersicht Sprayer Korpus München (Bestand Sammlung Kreuzer)",
	"4": "Übersicht Sprayer Korpus Köln",
	"5": "Übersicht Crews Köln",
	"6": "Übersicht Sprayer, Crews Korpus Polizei München",
	"7": "Übersicht Sprayer",
	"8": "Übersicht Lokalisierungen",
}

soup=BeautifulSoup(response.content,'lxml')

tables = soup.find_all('table')
# print(tables)

output_rows = []
numTable = 0
for table in tables:
	table_headers = []
	for tx in table.find_all('th'):
		table_headers.append(tx.text.replace("\\n", "").strip())
	for table_row in table.findAll('tr'):
		columns = table_row.findAll('td')
		output_row = []
		for column in columns:
			cell = column.text.replace("|", "").replace("\\n", "").strip()
			output_row.append(cell)
		if len(output_row) != 0:
			output_rows.append(output_row)
	
	# print(output_rows)
	with open(tableNames[str(numTable)]+'.csv', 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter='|')
		writer.writerow(table_headers)
		writer.writerows(output_rows)
	numTable = numTable + 1
