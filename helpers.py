import data

def __levenshtein(a,b):
  "Calculates the Levenshtein distance between a and b."
  n, m = len(a), len(b)
  if n > m:
    # Make sure n <= m, to use O(min(n,m)) space
    a,b = b,a
    n,m = m,n

  current = range(n+1)
  for i in range(1,m+1):
    previous, current = current, [i]+[0]*n
    for j in range(1,n+1):
      add, delete = previous[j]+1, current[j-1]+1
      change = previous[j-1]
      if a[j-1] != b[i-1]:
        change = change + 1
      current[j] = min(add, delete, change)

  return current[n]

def get_code_for_country(country):
  """Gets a country based on a user submitted search string"""
  codes = []
  for code, names in data.countries.iteritems():
    min_lev = min([__levenshtein(country.lower(), name.lower()) for name in names])
    codes.append({"code": code, "distance": min_lev})

  sorted_codes = sorted(codes,
    lambda x, y: cmp(
      x['distance'],
      y['distance']))
  return sorted_codes[0]['code']

def get_phone_for_code(code):
  """Gets the EMS phone for a country code"""
  if code in data.phone_for_country:
    return data.phone_for_country[code]
  else:
    return "911"

def get_name_for_disease(code):
  if code in data.disease_name_map:
    return data.disease_name_map[code]
  else:
    return "unknown disease"

def get_probability_for_disease(disease, country=None):
  if country:
    diseases = data.disease_prob_for_country[country]
    filtered_diseases = filter(lambda x: x['disease'] == disease.lower(), diseases)
    return filtered_diseases[0]['probability']
  else:
    return data.background_disease_probability[disease.lower()]

def get_symptom_probability(symptom_search):
  count = 0
  for disease, symptoms in data.symptoms_for_disease.iteritems():
    for symptom in symptoms:
      if symptom_search == symptom:
        count += 1
  return 1/float(count)

print get_symptom_probability("cough")
