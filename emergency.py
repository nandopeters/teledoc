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

def __get_nearest_distance(names, search_name):
  # sort alternate names for one country by the distance to the searched country
  sorted_names = sorted(names,
    lambda x,y: cmp(
      __levenshtein(x, search_name),
      __levenshtein(y, search_name)))
  nearest_name = sorted_names[0]
  distance = __levenshtein(search_name, nearest_name)
  return distance

def get_emergency_number_list():
  l = []
  with open('emergencyphones.csv', 'r') as f:
    for line in f:
      parts = line.replace('\n', '').split(',')
      l.append({ 'number': parts[0], 'names': parts[1:]})
  return l

def retrieve_emergency_number(number_list, country_name):
  # sort every number by the distance to the searched country
  sortednumber = sorted(number_list,
    lambda x,y: cmp(
      __get_nearest_distance(x['names'], country_name),
      __get_nearest_distance(y['names'], country_name)))
  return sortednumber[0]['number'], sortednumber[0]['names']

if __name__ == '__main__':
  number_list = get_emergency_number_list()
  print retrieve_emergency_number(number_list, 'United States')
