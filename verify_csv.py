import csv

def make_json():
	# Open a csv reader called DictReader
	with open('data.csv', encoding='utf-8') as csvf:
		csvReader = csv.DictReader(csvf)
		id = 0
		for rows in csvReader:
			id += 1
			# Assuming a column named 'No' to
			# be the primary key
			reg_no = rows['reg.no']
			if(reg_no == 'UIT1076'):
				print(rows['name'])

make_json()