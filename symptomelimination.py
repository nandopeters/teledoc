from diseases import read_country_diseases_prob_file, get_diseases_for_country
from symptomProbability import read_symptoms_file, get_symptoms_for_disease, get_symptom_probabilities

def calculate_probability_for_disease(country_disease_list, user_synthom_list, country_code,all_synthom_list):
  disease_probabilty = []
  diseases_in_country = get_diseases_for_country(country_disease_list, country_code)
  for disease in diseases_in_country:
    prob = 0
    for synthom in user_synthom_list:
      if synthom in get_symptoms_for_disease(all_synthom_list, disease['disease']):
        prob += disease["prob"] * get_symptom_probabilities(all_synthom_list,synthom)
    disease_probabilty.append({ 'disease': disease["disease"], 'prob': prob })
  return disease_probabilty

def get_ordered_symptom_list(diseasesproblist, symptomlist, country, answers):
  diseases = get_diseases_for_country(diseasesproblist, country)
  disease_probabilities = {}
  tmp = calculate_probability_for_disease(diseasesproblist, answers, country, symptomlist)
  for d in tmp:
    disease_probabilities[d['disease']] = d['prob']
  symptoms = {}
  for disease in diseases:
    tmp = get_symptoms_for_disease(symptomlist, disease['disease'])
    for symptom in tmp:
      if symptom in answers:
        continue
      sprob = get_symptom_probabilities(symptomlist, symptom)
      sprob *= disease_probabilities[disease['disease']]
      if symptom not in symptoms:
        symptoms[symptom] = sprob
      else:
        symptoms[symptom] += sprob
  return sorted([{'symptom': z[0], 'prob': z[1]} for z in symptoms.iteritems()], reverse=True, cmp=lambda x,y: cmp(x['prob'], y['prob']))

if __name__ =='__main__':
  diseasesproblist = read_country_diseases_prob_file()
  symptomlist = read_symptoms_file()
  print get_ordered_symptom_list(diseasesproblist, symptomlist, 'chn', ['fever', 'headache', 'malaise'])


