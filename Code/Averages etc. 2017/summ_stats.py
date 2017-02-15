import csv

def count_rejects(dataset, control, writeCsv):
    '''
    (list of dicts, bool, bool) => noneType
    counts and prints to screen the number of rejects in dataset. 
    control deals with the different cases of control vs. treatment group
    writeCsv deals with whether the results should be printed to file.
    '''
    rejectsC = 0
    rejectsU = 0
    dubious = 0
    

    for run in dataset:
        pvc = float(run['p_value_constrained'])
        pvu = float(run['p_value'])
        if pvc < 0.1:
            rejectsC += 1
        if pvu < 0.1:
            rejectsU += 1
        if pvc > pvu:
            dubious += 1
    
    if control == True:
        print ('Control group')
    else:
        print ('nu1 = ' + str (nu1) + ', nu2 = ' + str(nu2))
    # print ('Rejects for k > 1: ' + str(rejectsC))
    print ('Rejects for k > kmin: ' + str(rejectsU))
    # print ('pvc > pvu: ' + str(dubious))


       
def average_pvalues(dataset, control, writeCsv):
    '''
    (list of Dicts) => noneType
    computes averages of p-values in dataset, both for the control and treatment groups
    control deals with the different cases of control vs. treatment group
    writeCsv deals with whether the results should be printed to file.
    '''
    if writeCsv == True:
        outData = []
        
    sum_pvc = 0
    sum_pvu = 0
    denominator = len(dataset)

    for run in dataset:
        outRun = {}
        outRun['pvc'] = float(run['p_value_constrained'])
        outRun['pvu'] = float(run['p_value'])
        sum_pvc += float(run['p_value_constrained'])
        sum_pvu += float(run['p_value'])
            
        if control == True:
            outRun['nu1'] = 0.0
            outRun['nu2'] = 0.0
            outRun['control'] = True
        else:
            outRun['nu1'] = nu1
            outRun['nu2'] = nu2
            outRun['control'] = False
        
        if writeCsv == True:
            outData.append(outRun) 
        
    if control == True:
        print ('Control group')
    else:
        print ('nu1 = ' + str (nu1) + ', nu2 = ' + str(nu2))
    #print ('Average pvalue for k > 1: ' + str(sum_pvc/denominator))
    print ('Average pvalue for k >= kmin: ' + str(sum_pvu/denominator))
    
    if writeCsv == True:
        if control == False:
            outFileName = dirPathWrite + 'all_pvalues_onboarding' + str(control) + '_nu1_' + str(nu1) + '_nu2_' + str(nu2) +'.csv'
        else:
            outFileName = dirPathWrite + 'all_pvalues_onboarding' + str(control) + '.csv'
        with open (outFileName, 'w') as csvWriteFile:
            fieldnames = ['pvu', 'pvc', 'nu1', 'nu2', 'control']
            writer = csv.DictWriter(csvWriteFile, fieldnames = fieldnames)
            writer.writeheader()
            for run in outData:
                writer.writerow(run)

        
dirPath = '/Users/albertocottica/github/local/communities-network-design/Datasets/FittingData_02_2017/'
dirPathWrite = '/Users/albertocottica/github/local/communities-network-design/Stata files/Stata files 2017/'
writeCsv = False

distroData = []
control = True
with open(dirPath + 'Fitting_statistics_2000_1_False_1.0_100.csv', 'rU') as csvfile:
    distroReader = csv.DictReader(csvfile, delimiter = ';')
    for row in distroReader:
        distroData.append(row)
    
    
# count_rejects(distroData, control, writeCsv)
average_pvalues(distroData, control, writeCsv)

values = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

for nu1 in values:
    for nu2 in values:
        distroData = []
        control = False
        with open(dirPath + 'Fitting_statistics_2000_1_True_'+ str(nu1) + '_' + str(nu2) + '_1.0_100.csv', 'rU') as csvfile:
            distroReader = csv.DictReader(csvfile, delimiter = ';')
            for row in distroReader:
                distroData.append(row)
        # count_rejects(distroData, control, writeCsv)
        average_pvalues(distroData, control, writeCsv)
    print ('=========================================')
      




    