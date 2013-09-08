from diseases import get_diseases_for_country,read_diseases_prob_file,read_country_diseases_prob_file
from symptomProbability import read_symptoms_file, get_symptoms_for_disease, get_symptom_probabilities

def calculate_probability_for_disease(country_disease_list, user_synthom_list, country_code,all_synthom_list):
  disease_probabilty = []
  diseases_in_country = get_diseases_for_country(country_disease_list, country_code)
  print diseases_in_country
  for disease in diseases_in_country:
    prob = 0
    for synthom in user_synthom_list:
	    prob += disease["prob"] * get_symptom_probabilities(all_synthom_list,synthom)
    disease_probabilty.append({ 'disease': disease["disease"], 'prob': prob })
  return disease_probabilty

if __name__ == '__main__':
  pass
  list = read_symptoms_file()

  print get_symptom_probabilities(list, "cough")
  data = read_country_diseases_prob_file()

  print calculate_probability_for_disease(data,['fever','cough'], 'mdg',list)
