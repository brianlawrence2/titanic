import csv as csv
import numpy as np

# Open up the csv file in to a Python object
test_file_object = csv.reader(open('../data/test.csv', 'rb'))
header = test_file_object.next()

open_file_object = csv.writer(open("../submissions/genderbasedmodel.py", "wb"))

for row in test_file_object:
  if row[2] == 'female':
    row.insert(0,'1')

    open_file_object.writerow(row)
  else:
    row.insert(0,'0')
    open_file_object.writerow(row)
