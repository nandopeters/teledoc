from data import countries, phone_for_country

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
  for code, names in countries.iteritems():
    min_lev = min([__levenshtein(country.lower(), name.lower()) for name in names])
    codes.append({"code": code, "distance": min_lev})

  sorted_codes = sorted(codes,
    lambda x, y: cmp(
      x['distance'],
      y['distance']))
  return sorted_codes[0]['code']

def get_phone_for_code(code):
  """Gets the EMS phone for a country code"""
  return phone_for_country[code]
