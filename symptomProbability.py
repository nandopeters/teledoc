import csv

def read_symptoms_file(filename):
  l = []
  with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='#')
    for row in csvreader:
      l.append(row)
  return l
  
def get_symptom_probabilities(list, symptom):
    count = 0
    for row in list:
      for i in range(0, len(row)):
        if row[i] == symptom:
          count += 1
    return 1/float(count)

if __name__ == '__main__':
  list = read_symptoms_file("data/symptoms.txt")
  print get_symptom_probabilities(list, "cough")