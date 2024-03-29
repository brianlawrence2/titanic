import csv as csv
import numpy as np

# Open up the csv file in to a Python object
csv_file_object = csv.reader(open('../data/train.csv', 'rb'))
header = csv_file_object.next()

data = []
for row in csv_file_object:
  data.append(row)
data = np.array(data)

number_passengers = np.size(data[0::,0].astype(np.float))
number_survived = np.sum(data[0::,0].astype(np.float))
proportion_survivors = number_survived / number_passengers

women_only_stats = data[0::,3] == "female"

men_only_stats = data[0::,3] != "female"

women_onboard = data[women_only_stats,0].astype(np.float)
men_onboard = data[men_only_stats,0].astype(np.float)

proportion_women_survived = np.sum(women_onboard) / np.size(women_onboard)
proportion_men_survived = np.sum(men_onboard) / np.size(men_onboard)

print 'Proportion of women who survived is %s' % proportion_women_survived
print 'Proportion of men who survived is %s' % proportion_men_survived
