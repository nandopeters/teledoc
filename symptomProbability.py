import csv

def read_symptoms_file():
  l = []
  with open("data/symptoms.txt", 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='#')
    for row in csvreader:
      l.append(row)
  return l

def get_symptoms_for_disease(list, disease):
  for row in list:
    if row[0] == disease:
      return row[1:]
  return []

def get_symptom_probabilities(list, symptom):
    count = 0
    for row in list:
      for i in range(0, len(row)):
        if row[i] == symptom:
          count += 1
    return 1/float(count)

if __name__ == '__main__':
  list = read_symptoms_file()
  print get_symptom_probabilities(list, "cough")