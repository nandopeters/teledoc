from diseases import read_country_diseases_prob_file, get_diseases_for_country
from symptomProbability import read_symptoms_file, get_symptoms_for_disease, get_symptom_probabilities

def get_ordered_symptom_list(diseasesproblist, symptomlist, country, answers):
  diseases = get_diseases_for_country(diseasesproblist, country)
  symptoms = {}
  for disease in diseases:
    tmp = get_symptoms_for_disease(symptomlist, disease['disease'])
    for symptom in tmp:
      sprob = get_symptom_probabilities(symptomlist, symptom)
      if symptom not in symptoms:
        symptoms[symptom] = disease['prob'] * sprob
      else:
        symptoms[symptom] *= disease['prob']
  return sorted([{'disease': z[0], 'prob': z[1]} for z in symptoms.iteritems()], reverse=True, cmp=lambda x,y: cmp(x['prob'], y['prob']))

if __name__ =='__main__':
  diseasesproblist = read_country_diseases_prob_file()
  symptomlist = read_symptoms_file()
  print get_ordered_symptom_list(diseasesproblist, symptomlist, 'deu', [])


