import csv

countries = {}
reader = csv.reader(open('data/countries.csv', 'rb'))
for row in reader:
  countries[row[0].strip()] = filter(bool, set([v.strip() for v in row[1:]]))


phone_for_country = {}
reader = csv.reader(open('data/phone_for_country.csv', 'rb'))
for row in reader:
  phone_for_country[row[0].strip()] = row[1].strip()
