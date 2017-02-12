import os
import powerlaw
import random as rd
import datetime
from pylab import *
import matplotlib.pyplot as pyplot
from matplotlib.legend_handler import HandlerLine2D
import collections
import math

#csv = "res.csv"
#csv = "res_wob.csv"

folders = ["../Datasets/FittingData_02_2017/"]
initiated = False


def __drawCCDF(data_serie, table_y_label, plot_title, xmin=None, other=False, legend=["pvalue=0", "pvalue!=0"]):
        #print 'Plotting PDF - ',plot_title
        global initiated

        

        # cosmetics setting
        default_empiric = 'blue'
        default_ccdf_linewidth = 1.0
        default_ccdf_fit_linestyle = '--'
        default_other = 'red'
        default_fit = 'green'
        default_otherfit = 'orange'

        if initiated == False:
        # now draws the CCDF against the powerlaw
            plt.figure("PDF - " + plot_title)
            plt.title("PDF - " + plot_title)
            plt.xlabel(table_y_label)
            plt.grid()

            empiric_rec = plt.Line2D((0,1),(0,0), color=default_empiric, linestyle='-')
            fit_rec = plt.Line2D((0,1),(0,0), color=default_fit, linestyle='--')
            other_rec = plt.Line2D((0,1),(0,0), color=default_other, linestyle='-')
            otherfit_rec = plt.Line2D((0,1),(0,0), color=default_otherfit, linestyle='--')

            # places the legend on the bottom left corner
            first_legend = plt.legend([empiric_rec, fit_rec, other_rec, otherfit_rec],[legend[0], 'fit '+legend[0], legend[1], 'fit '+legend[1]], loc=3)
            initiated = True


        # do different fits (should be optional in the future)
        if xmin == None:
            fit = powerlaw.Fit(data_serie, discrete=True)
        else:
            fit = powerlaw.Fit(data_serie, discrete=True, xmin=xmin)

        if other == True:
            default_empiric = default_other
            default_fit = default_otherfit


        plot1 = fit.plot_pdf(color=default_empiric, \
                                linewidth=default_ccdf_linewidth,\
                                label='empirical', alpha=0.2)

        #plot2 = fit.exponential.plot_pdf (color=default_ccdf_exponential_color, \
        #                                   linewidth=default_ccdf_linewidth, \
        #                                   ls=default_ccdf_fit_linestyle, \
        #                                   label='exponential')

        plot3 = fit.power_law.plot_pdf (color = default_fit, \
                                         linewidth=default_ccdf_linewidth, \
                                         ls=default_ccdf_fit_linestyle, \
                                         label='powerlaw', alpha=0.2)

        #plot4 = fit.lognormal.plot_pdf (color = default_ccdf_lognormal_color, \
        #                                 linewidth=2.0, \
        #                                 ls=default_ccdf_fit_linestyle, \
        #                                 label='lognormal')


        # if we want the distances of fit, here they are
        # print fit.distribution_compare('power_law', 'lognormal', normalized_ratio=True)
        # maybe find a way to automatically extract the top n%

        # do not forget the grid!


def dumpPlot(plot_title):
    global initiated        
    plt.savefig('./images/'+ "PDF_" + plot_title.replace(' ', '_')+'.png',\
                format="png",\
                dpi=100)
    plt.gcf().clear()
    initiated = False


def __computeDegreeDistribution(degree_list, frequency=False, dict_form=False, ma=True):
    if ma:
        degree_list = [d+1 for d in degree_list]

    counted = collections.Counter(sorted(degree_list))
    counter = collections.OrderedDict(sorted(counted.items()))

    if dict_form:
        if frequency:
            n = float(len(degree_list))
            for k in counter:
                couter[k] /= n
            return counter
        else:
            return counter


    if frequency:
        n = float(len(degree_list))
        return {"indegree":counter.keys(), "count":[x/n for n in counter.values()]}
    else:
        return {"indegree":counter.keys(), "count":counter.values()}

    #print(counter)
    # Counter({1: 4, 2: 4, 3: 2, 5: 2, 4: 1})
    #print(counter.values())
    # [4, 4, 2, 1, 2]
    #print(counter.keys())


initiated = False

# this function draws a distribution (basicaly just a plot x/y)
def __drawDistribution(data, table_x_label, table_y_label, plot_title, color="blue"):

        global initiated

        #plt.figure("Distribution - " + plot_title)
        #plt.title("Distribution - " + plot_title)
        #plt.xlabel(table_x_label)
        #plt.ylabel(table_y_label)

        if initiated == False:

            x_values = [x+1 for x in data[table_x_label]]
            y_values = data[table_y_label]
            #print data

            #plt.plot(x_values, y_values)
            plt.figure("Distribution - " + plot_title)
            ax = plt.subplot(111)

            plt.title("Distribution - " + plot_title)
            plt.xlabel(table_x_label)
            plt.ylabel(table_y_label)
            #plt.ylim(min(y_values), max(y_values))
            #plt.xlim(0, 100)
            plt.grid()
            initiated = False

        line, = ax.plot(x_values, y_values, color=color, alpha=0.2)#, marker='o')#, color='blue', lw=2)
        ax.set_xscale('log')
        ax.set_yscale('log')


def read_csv(lines, nu1=None, nu2=None, WOB=True, verbose=False):
    print nu1, nu2
    
    entries = [l.split(';') for l in lines]
    #print 'the entries are ', entries[0]
    #print "the rest is ", entries[1]

    #['alpha_constrained', 'sigma_constrained', 'p_value_constrained', 'alpha', 'sigma', 'p_value', 'x_min']
    alpha_constrained = [l[0] for l in entries]
    sigma_constrained = [l[1] for l in entries]
    pvalue_constrained = [l[2] for l in entries]
    alpha_unconstrained = [l[3] for l in entries]
    sigma_unconstrained = [l[4] for l in entries]
    pvalue_unconstrained = [l[5] for l in entries]
    xmin_unconstrained = [l[6] for l in entries]
    distribution = [l[7] for l in entries]

    for e in entries[1:]:
        #print e[2]
        distribution = eval(e[7])
        test = e[2]
        #test = e[5]
        legend = ["pv_unconst=0","pv_unconst!=0"]

        if float(test) == 0.0:# and float(test) != 1.0:
            #print "p_value is null"
            distribution = eval(e[7])
            #__drawDistribution(__computeDegreeDistribution(distribution), "indegree", "count", "fit")
            __drawCCDF(distribution, "indegree", "fit nu1=%.2f nu2=%.2f wob=%s %s"%(nu1,nu2,WOB,legend[0]), legend=legend)
        else:
            __drawCCDF(distribution, "indegree", "fit nu1=%.2f nu2=%.2f wob=%s %s"%(nu1,nu2,WOB,legend[0]), other=True, legend=legend)
            #__drawDistribution(__computeDegreeDistribution(distribution), "indegree", "count", "fit", "red")


    dumpPlot("fit nu1=%.2f nu2=%.2f wob=%s %s"%(nu1,nu2,WOB,legend[0]))
        #if float(test) == 1.0:
        #    print "p-value is one"

    #plt.show()

    '''

    avg_alpha_constrained = sum([float(i) for i in alpha_constrained[1:] if i != 'alpha_constrained'])/(len(alpha_constrained)-1)
    avg_alpha_unconstrained = sum([float(i) for i in alpha_unconstrained[1:] if i != 'alpha'])/(len(alpha_constrained)-1)
    avg_sigma_unconstrained = sum([float(i) for i in sigma_unconstrained[1:] if i != 'sigma'])/(len(alpha_constrained)-1)
    avg_sigma_constrained = sum([float(i) for i in sigma_constrained[1:] if i != 'sigma_constrained'])/(len(alpha_constrained)-1)
    avg_pvalue_constrained = sum([float(i) for i in pvalue_constrained[1:] if i != 'p_value_constrained'])/(len(alpha_constrained)-1)
    avg_pvalue_unconstrained = sum([float(i) for i in pvalue_unconstrained[1:] if i != 'p_value'])/(len(alpha_constrained)-1)

    if verbose:
        print 'avg_alpha_constrained:',avg_alpha_constrained
        print 'avg_sigma_constrained:',avg_sigma_constrained
        print 'avg_pvalue_constrained:',avg_pvalue_constrained
        print 'avg_alpha_unconstrained:',avg_alpha_unconstrained
        print 'avg_sigma_unconstrained:',avg_sigma_unconstrained
        print 'avg_pvalue_unconstrained:',avg_pvalue_unconstrained

    return {'constrained':{'alpha':avg_alpha_constrained, 'sigma':avg_sigma_constrained, 'p-value':avg_pvalue_constrained},
            'unconstrained':{'alpha':avg_alpha_unconstrained, 'sigma':avg_sigma_unconstrained, 'p-value':avg_pvalue_unconstrained}}
    '''

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
    csv_files = sorted([f for f in os.listdir(folder) if 'csv' in f])

    for f in csv_files:
        p = read_parameters(f)
        runclass = "%d_%f_%s_%s_%s_%f_%d"%(p['nbnodes'],p['m'],p['onboard'],p['nu1'],p['nu2'],p['a'],p['nbruns'])
        if runclass not in classToFiles:
            classToFiles[runclass]=[]
        classToFiles[runclass].append(folder+f)

output_folder =  "concatenate/"

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
    nu1 = float(entries[3])
    nu2 = float(entries[4])
    wob = entries[2] == 'True'
    results = read_csv(total_lines, nu1, nu2, wob) 
    #print c, 'unconstrained: ',results['unconstrained']['p-value'], 'constrained: ',results['constrained']['p-value']
#plt.show()
    
