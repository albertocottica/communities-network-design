## build a file with: run number (1 to 100), control/treatment, nu1/nu2, pvalues

import csv

dirPath = '/Users/albertocottica/github/local/communities-network-design/Datasets/FittingData_02_2017/'
dirPathWrite = '/Users/albertocottica/github/local/communities-network-design/Stata files/Stata files 2017/'

def load_control_group():
    distroData = []
    with open(dirPath + 'Fitting_statistics_2000_1_False_1.0_100.csv', 'rU') as csvfile:
        distroReader = csv.DictReader(csvfile, delimiter = ';')
        runCounter = 0 
        for row in distroReader:
            oneObs = {}
            oneObs['type'] = 'control'
            oneObs['run'] = runCounter
            for key in row:
                if key != 'original_degree_distribution':
                    oneObs[key] = row[key]            
            distroData.append(oneObs)
            runCounter += 1
            
    # copy the generated observations 16 times, assigning them different combinations of nu1 and nu2
    expandedData = []
    for i in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        for j in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
            for row in distroData:
                row['nu1'] = i
                row['nu2'] = j
                expandedData.append(row)
    return expandedData
    
def load_treatment_group():
    values = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    enrichedData = []
    for nu1 in values:
        for nu2 in values:

            with open(dirPath + 'Fitting_statistics_2000_1_True_'+ str(nu1) + '_' + str(nu2) + '_1.0_100.csv', 'rU') as csvfile:
                distroReader = csv.DictReader(csvfile, delimiter = ';')
                runCounter = 0 
                for row in distroReader:
                    oneObs = {}
                    oneObs['nu1'] = nu1
                    oneObs['nu2'] = nu2
                    oneObs['type'] = 'treatment'
                    oneObs['run'] = runCounter
                    for key in row:
                        if key != 'original_degree_distribution':
                            oneObs[key] = row[key] 
                    enrichedData.append(oneObs)
                    runCounter += 1
            
    return enrichedData
    
def dictWrite(source):
    '''
    (list of dicst) => noneType
    writes source as a csv file
    '''
    fieldnames = []
    for key in source[0]:
        fieldnames.append(key)
    
    with open (dirPathWrite + 'data4Stata.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        for item in source:
            writer.writerow(item)
    
cG= load_control_group()
tG = load_treatment_group()
allData = cG + tG

dictWrite(allData)