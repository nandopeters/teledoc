from csvreader import readcsv

def read_country_diseases_prob_file():
  return readcsv('data/disease_prob_for_country.csv')
  
def read_diseases_prob_file():
  return readcsv('data/background_prob_disease.csv')

def get_diseases_for_country(country_disease_list, country_code):
  disease_codes =[]
  for disease in country_disease_list:
    if disease['country'] == country_code:
      disease_codes.append({ 'disease': disease['disease'], 'prob': float(disease['prob']) })
  return disease_codes

def get_disease_prob(disease_list, disease_code):
  for disease in disease_list:
    if disease['disease'] == disease_code:
      return float(disease['prob'])

if __name__ == '__main__':
  #data = read_country_diseases_prob_file()
  #print get_diseases_for_country(data, 'deu')
  data = read_diseases_prob_file()
  print get_disease_prob(data, 'whs3_42')
