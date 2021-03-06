import data
import helpers
import fileinput

def calculate_probability_for_disease(country, user_symptom_list):
  """Returns diseases based on symptoms the user has"""
  disease_probabilty = []
  diseases_in_country = data.disease_prob_for_country[country]
  normalizing_term = 0
  for disease in diseases_in_country:
    prob = 0
    if len(user_symptom_list) == 0:
      prob = helpers.get_probability_for_disease(disease['disease'],country)
    else:
      for symptom in user_symptom_list:
        if symptom in data.symptoms_for_disease[disease['disease']]:
          prob += disease["probability"] * helpers.get_symptom_probability(symptom)
    normalizing_term += prob
    disease_probabilty.append({ 'disease': disease["disease"], 'probability': prob })
  for disease in disease_probabilty:
    disease["probability"] /= normalizing_term
  return disease_probabilty

def get_ordered_symptom_list(country, user_symptom_list, symptom_blacklist):
  """Returns symptoms to ask the user about based on existing symptoms and location"""
  diseases = data.disease_prob_for_country[country]
  disease_probabilities = {}
  tmp = calculate_probability_for_disease(country, user_symptom_list)
  for d in tmp:
    disease_probabilities[d['disease']] = d['probability']
  symptoms = {}
  for disease in diseases:
    tmp = data.symptoms_for_disease[disease['disease']]
    for symptom in tmp:
      if symptom in user_symptom_list:
        continue
      if symptom in symptom_blacklist:
        continue
      sprob = helpers.get_symptom_probability(symptom)
      sprob *= disease_probabilities[disease['disease']]
      if symptom not in symptoms:
        symptoms[symptom] = sprob
      else:
        symptoms[symptom] += sprob
  return sorted([{'symptom': z[0], 'prob': z[1]} for z in symptoms.iteritems()], reverse=True, cmp=lambda x,y: cmp(x['prob'], y['prob']))
