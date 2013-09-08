from csvreader import readcsv

def read_diseases_prob_file():
  return readcsv('data/disease_prob_for_country.csv')

def get_diseases_for_country(country_disease_list, country_code):
  disease_codes =[]
  for disease in country_disease_list:
    if disease['country'] == country_code:
      disease_codes.append({ 'disease': disease['disease'], 'prob': float(disease['prob']) })
  return disease_codes

if __name__ == '__main__':
  data = read_diseases_prob_file()
  print get_diseases_for_country(data, 'deu')

