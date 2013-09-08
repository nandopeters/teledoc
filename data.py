import csv

countries = {}
reader = csv.reader(open('data/countries.csv', 'rb'))
for row in reader:
  countries[row[0].strip()] = filter(bool, set([v.strip() for v in row[1:]]))


phone_for_country = {}
reader = csv.reader(open('data/phone_for_country.csv', 'rb'))
for row in reader:
  phone_for_country[row[0].strip()] = row[1].strip()

disease_prob_for_country = {}
reader = csv.DictReader(open('data/disease_prob_for_country.csv', 'rb'))
for row in reader:
  country = row['country'].upper()
  if country in disease_prob_for_country:
    disease_prob_for_country[country].append({"disease": row['disease'].lower(), 'probability': float(row['prob'])})
  else:
    disease_prob_for_country[country] = [{"disease": row['disease'].lower(), 'probability': float(row['prob'])}]

background_disease_probability = {}
reader = csv.DictReader(open('data/background_prob_disease.csv', 'rb'))
for row in reader:
  background_disease_probability[row['disease'].lower()] = float(row['prob'])

disease_name_map = {}
reader = csv.DictReader(open('data/disease_code_to_name.csv', 'rb'))
for row in reader:
  disease_name_map[row['code'].lower()] = row['name']

symptoms_for_disease = {}
reader = csv.reader(open("data/symptoms.csv", 'r'), delimiter=',', quotechar='"')
for row in reader:
  symptoms_for_disease[row[0].lower()] = row[1:]
