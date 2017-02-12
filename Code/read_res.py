import os
#csv = "res.csv"
#csv = "res_wob.csv"

folders = ["distant-results/", "results/", "../Datasets/FittingData_02_2017/"]
folders = ["../Datasets/FittingData_02_2017/"]
folders = ["../Datasets/FittingData/"]


def read_csv(lines, verbose=False):
    
    entries = [l.split(';') for l in lines]
    print 'the entries are ', len(entries[0]), entries[0]
    #print "the rest is ", entries[1]

    #['alpha_constrained', 'sigma_constrained', 'p_value_constrained', 'alpha', 'sigma', 'p_value', 'x_min']
    if len(entries[0]) > 5:
        alpha_constrained = [l[0] for l in entries]
        sigma_constrained = [l[1] for l in entries]
        pvalue_constrained = [l[2] for l in entries]
        alpha_unconstrained = [l[3] for l in entries]
        sigma_unconstrained = [l[4] for l in entries]
        pvalue_unconstrained = [l[5] for l in entries]
        xmin_unconstrained = [l[6] for l in entries]        

        avg_alpha_constrained = sum([float(i) for i in alpha_constrained[1:] if i != 'alpha_constrained'])/(len(alpha_constrained)-1)
        avg_alpha_unconstrained = sum([float(i) for i in alpha_unconstrained[1:] if i != 'alpha'])/(len(alpha_constrained)-1)
        avg_sigma_unconstrained = sum([float(i) for i in sigma_unconstrained[1:] if i != 'sigma'])/(len(alpha_constrained)-1)
        avg_sigma_constrained = sum([float(i) for i in sigma_constrained[1:] if i != 'sigma_constrained'])/(len(alpha_constrained)-1)
        avg_pvalue_constrained = sum([float(i) for i in pvalue_constrained[1:] if i != 'p_value_constrained'])/(len(alpha_constrained)-1)
        avg_pvalue_unconstrained = sum([float(i) for i in pvalue_unconstrained[1:] if i != 'p_value'])/(len(alpha_constrained)-1)
    else:
        alpha_constrained = [l[0] for l in entries]
        pvalue_constrained = [l[1] for l in entries]
        alpha_unconstrained = [l[2] for l in entries]
        pvalue_unconstrained = [l[3] for l in entries]
        xmin_unconstrained = [l[4] for l in entries]        

        avg_alpha_constrained = sum([float(i) for i in alpha_constrained[1:] if i != 'alpha_constrained'])/(len(alpha_constrained)-1)
        avg_alpha_unconstrained = sum([float(i) for i in alpha_unconstrained[1:] if i != 'alpha'])/(len(alpha_constrained)-1)
        avg_pvalue_constrained = sum([float(i) for i in pvalue_constrained[1:] if i != 'p_value_constrained'])/(len(alpha_constrained)-1)
        avg_pvalue_unconstrained = sum([float(i) for i in pvalue_unconstrained[1:] if i != 'p_value'])/(len(alpha_constrained)-1)
        avg_sigma_unconstrained = None#sum([float(i) for i in sigma_unconstrained[1:] if i != 'sigma'])/(len(alpha_constrained)-1)
        avg_sigma_constrained = None#sum([float(i) for i in sigma_constrained[1:] if i != 'sigma_constrained'])/(len(alpha_constrained)-1)

    if verbose:
        print 'avg_alpha_constrained:',avg_alpha_constrained
        print 'avg_sigma_constrained:',avg_sigma_constrained
        print 'avg_pvalue_constrained:',avg_pvalue_constrained
        print 'avg_alpha_unconstrained:',avg_alpha_unconstrained
        print 'avg_sigma_unconstrained:',avg_sigma_unconstrained
        print 'avg_pvalue_unconstrained:',avg_pvalue_unconstrained

    return {'constrained':{'alpha':avg_alpha_constrained, 'sigma':avg_sigma_constrained, 'p-value':avg_pvalue_constrained},
            'unconstrained':{'alpha':avg_alpha_unconstrained, 'sigma':avg_sigma_unconstrained, 'p-value':avg_pvalue_unconstrained}}

def read_parameters(filename):
    #Fitting_statistics_2000_1_False_1.0_2500.csv
    #New_Fitting_statistics_2000_1_True_0.0_0.0_1.0_2500.csv
    #New_Fitting_statistics_2000_1_True_0.0_0.2_1.0_2500.csv

    parameters = filename.split('.csv')
    entries = parameters[0].replace("New_","").replace("Fitting_statistics_", "").split("_")
    #print entries
    nbnodes = int(entries[0])
    m = int(entries[1])
    onboard = entries[2] == "True"
    nu1 = None
    nu2 = None
    if onboard == True:
        nu1 = float(entries[3])
        nu2 = float(entries[4])
        a = float(entries[5])
        nbruns = int(entries[6])
    else:
        a = float(entries[3])
        nbruns = int(entries[4])

    return {'nbnodes': nbnodes, 'm':m, 'onboard':onboard, 'nu1':nu1, 'nu2':nu2, 'a':a, 'nbruns':nbruns}
    
classToFiles = {}

for folder in folders:
    csv_files = sorted([f for f in os.listdir(folder) if 'csv' in f and "Fitting" in f and 'all' not in f])

    for f in csv_files:
        print f
        p = read_parameters(f)
        runclass = "%d_%f_%s_%s_%s_%f_%d"%(p['nbnodes'],p['m'],p['onboard'],p['nu1'],p['nu2'],p['a'],p['nbruns'])
        if runclass not in classToFiles:
            classToFiles[runclass]=[]
        classToFiles[runclass].append(folder+f)

output_folder =  "concatenate/"

results_nu1 = {}
results_nu2 = {}
#2000_1.000000_True_1.0_0.8_1.000000_2500

for c in sorted(classToFiles):
    print "processing class ", c, " with ", len(classToFiles[c]), "files"
    total_lines = []
    for csv in classToFiles[c]:
        print "reading file ",csv
        with open(csv) as f:
            text = f.read().rstrip().replace('\r','\n')
            #for l in f:
            #    print l

            total_lines += text.split('\n')

    entries = c.split('_')
    nu_1 = float(entries[3])
    nu_2 = float(entries[4])
    n = int(entries[6])
    results = read_csv(total_lines) 
    print n, nu_1, nu_2, 'unconstrained:',results['unconstrained']['p-value'], 'constrained:',results['constrained']['p-value']

    if nu_1 not in results_nu1:
        results_nu1[nu_1] = {}
    results_nu1[nu_1][nu_2] = results
    if nu_2 not in results_nu2:
        results_nu2[nu_2] = {}
    results_nu2[nu_2][nu_1] = results

for nu1 in sorted(results_nu1):
    pvalues = []
    pvalues_constrained = []
    for nu2 in sorted(results_nu1[nu1]):
        res=results_nu1[nu1][nu2]
        pvalues.append(res['unconstrained']['p-value'])
    print "nu1 ",nu1, '(', sum(pvalues)/len(pvalues) ,')', pvalues
for nu1 in sorted(results_nu1):
    pvalues = []
    pvalues_constrained = []
    for nu2 in sorted(results_nu1[nu1]):
        res=results_nu1[nu1][nu2]
        pvalues_constrained.append(res['constrained']['p-value'])
    print "nu1 ",nu1, '(', sum(pvalues_constrained)/len(pvalues_constrained) ,')', pvalues_constrained
    

for nu2 in sorted(results_nu2):
    pvalues = []
    pvalues_constrained = []
    for nu1 in sorted(results_nu2[nu2]):
        res=results_nu2[nu2][nu1]
        pvalues.append(res['unconstrained']['p-value'])
    print "nu2 ",nu2, '(', sum(pvalues)/len(pvalues) ,')', pvalues
for nu2 in sorted(results_nu2):
    pvalues = []
    pvalues_constrained = []
    for nu1 in sorted(results_nu2[nu2]):
        res=results_nu2[nu2][nu1]
        pvalues_constrained.append(res['constrained']['p-value'])
    print "nu2 ",nu2, '(', sum(pvalues_constrained)/len(pvalues_constrained) ,')', pvalues_constrained
    
