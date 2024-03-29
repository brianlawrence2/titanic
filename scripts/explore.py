import csv as csv
import numpy as np

# Open up the csv file in to a Python object
csv_file_object = csv.reader(open('../data/train.csv', 'rb'))
header = csv_file_object.next()

data = []
for row in csv_file_object:
  data.append(row)
data = np.array(data)

fare_ceiling = 40
data[data[0::,8].astype(np.float) >= fare_ceiling, 8] = fare_ceiling-1.0
fare_bracket_size = 10
number_of_price_brackets = fare_ceiling / fare_bracket_size
number_of_classes = 3
survival_table = np.zeros((2, number_of_classes, number_of_price_brackets))

for i in xrange(number_of_classes):
  for j in xrange(number_of_price_brackets):

    women_only_stats = data[
        (data[0::,3] == "female")
        & (data[0::,1].astype(np.float) == i+1)
        & (data[0::,8].astype(np.float) >= j*fare_bracket_size)
        & (data[0::,8].astype(np.float) < (j+1)*fare_bracket_size), 0]

    men_only_stats = data[
        (data[0::,3] != "female")
        & (data[0::,1].astype(np.float) == i+1)
        & (data[0::,8].astype(np.float) >= j*fare_bracket_size)
        & (data[0::,8].astype(np.float) < (j+1)*fare_bracket_size), 0]

    survival_table[0,i,j] = np.mean(women_only_stats.astype(np.float))
    survival_table[1,i,j] = np.mean(men_only_stats.astype(np.float))

survival_table[ survival_table != survival_table ] = 0
survival_table[ survival_table < 0.5 ] = 0
survival_table[ survival_table >= 0.5 ] = 1

test_file_object = csv.reader(open('../data/test.csv', 'rb'))
fname = '../submissions/genderclasspricebasedmodelpy.csv'
open_file_object = csv.writer(open(fname, 'wb'))
header = test_file_object.next()

for row in test_file_object:
  for j in xrange(number_of_price_brackets):
    try:
      row[7] = float(row[7])
    except:
      bin_fare = 3-float(row[0])
      break
    if row[7] > fare_ceiling:
      bin_fare = number_of_price_brackets-1
      break
    if row[7] >= j*fare_bracket_size and row[7] < (j+1)*fare_bracket_size:
      bin_fare = j
      break

  if row[2] == 'female':
    row.insert(0, int(survival_table[0,float(row[0])-1,bin_fare]))
    open_file_object.writerow(row)
  else:
    row.insert(0,int(survival_table[1,float(row[0])-1,bin_fare]))
    open_file_object.writerow(row)
