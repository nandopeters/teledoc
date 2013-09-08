import csv

def readcsv(filename):
  with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='#')
    headers = []
    content = []
    for row in csvreader:
      if len(headers) == 0:
        headers = row
      else:
        data = {}
        for i in range(0, len(row)):
          data[headers[i]] = row[i]
        content.append(data)
    return content
