import csv

def __uniq(seq):
  seen = set()
  seen_add = seen.add
  return [ x for x in seq if x not in seen and not seen_add(x)]

supported_countries = []

countries = {}
reader = csv.reader(open('data/countries.csv', 'rb'))
for row in reader:
  supported_countries.append(row[0].strip())
  countries[row[0].strip()] = filter(bool, __uniq([v.strip() for v in row[1:]]))

phone_for_country = {}
_temp = []
reader = csv.reader(open('data/phone_for_country.csv', 'rb'))
for row in reader:
  _temp.append(row[0].strip())
  phone_for_country[row[0].strip()] = row[1].strip()

supported_countries = set(supported_countries).intersection(set(_temp))

disease_prob_for_country = {}
_temp = []
reader = csv.DictReader(open('data/disease_prob_for_country.csv', 'rb'))
for row in reader:
  country = row['country'].upper()
  _temp.append(country)
  if country in disease_prob_for_country:
    disease_prob_for_country[country].append({"disease": row['disease'].lower(), 'probability': float(row['prob'])})
  else:
    disease_prob_for_country[country] = [{"disease": row['disease'].lower(), 'probability': float(row['prob'])}]

supported_countries = set(supported_countries).intersection(set(_temp))

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

symptoms = []
for disease, disease_symptoms in symptoms_for_disease.iteritems():
  symptoms = symptoms+disease_symptoms

symptoms = list(set(symptoms))

