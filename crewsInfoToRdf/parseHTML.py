from bs4 import BeautifulSoup
import requests
import csv


authUrl = 'https://wikis.uni-paderborn.de/graffiti/index.php?title=Spezial:Anmelden&returnto=Informationen zu den Namen (Pseudonymen)'
auth = requests.post(authUrl, params={'wpName': '', 'wpPassword': '', 'authAction': 'login'})
print(auth)

headers = {
'Cookie': ''
}

url = 'https://wikis.uni-paderborn.de/graffiti/Informationen_zu_den_Namen_(Pseudonymen)' #'https://en.wikipedia.org/wiki/List_of_English_football_champions'
response=requests.get(url, headers=headers)

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
		table_headers.append(tx.text.strip())
	for table_row in table.findAll('tr'):
		columns = table_row.findAll('td')
		output_row = []
		for column in columns:
			output_row.append(column.text.replace("|", "").replace("\n", "").strip())
		if len(output_row) != 0:
			output_rows.append(output_row)
	
	# print(output_rows)
	with open(tableNames[str(numTable)]+'.csv', 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter='|')
		writer.writerow(table_headers)
		writer.writerows(output_rows)
	numTable = numTable + 1
