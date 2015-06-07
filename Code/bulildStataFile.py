# building the general dataset for Stata

import csv
import numpy as np

dirPath = '/Users/albertocottica/github/local/communities-network-design/Datasets/FittingData/'
outFile = open(dirPath + 'allFittingData.csv', 'w')

allData = []


fieldNames = ['nu1','nu2','exp_all', 'p-value_all', 'exp', 'p_value', 'kmin']
allData.append(fieldNames)
		
for i in np.arange (0.0,1.1,0.2):
	for j in np.arange(0.0,1.1,0.2):
		# open the file 
		fileName = 'Fitting_statistics_2000_1_True_' + str(i) + '_' + str(j) + '_1.0_2500.csv'
		csvFile = open (dirPath + fileName, 'r')
		genericRow =[i,j] # the generic datarow
		csv_reader = csv.reader (csvFile, delimiter = ',')
		for row in csv_reader:
#			if not type(row[0])== float:
#				continue
			for k in range(5):
				genericRow.append(row[k])
			genericRow.append(row) 
		allData.append(genericRow)
		csvFile.close()
		
		
csv.writer(outFile).writerows(allData)
outFile.close()