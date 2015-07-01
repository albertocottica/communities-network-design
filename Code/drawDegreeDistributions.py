# draws degree distributions

# needs a backend for MatPlotLib. I run the code from iPython.
# to do this: copy the code from the script file, then use the cpaste command in iPython
# the object "data" is a list of degrees. Replace your own.

import powerlaw

# insert data here data = []
path = '/Users/albertocottica/github/local/communities-network-design/Datasets/GeneratedDegrees/'
fName = 'DegreesOfOnBoardingModel_with_onboarding_size_2000_m_1_a_1_alpha_0.400000_gamma_0.800000.json'
# not really a json, opening as text file with a single line 
f = open (path + fName, 'rU')
data = f.read().strip()
data = data[1:len(data)-1].split(', ')
data = map(lambda x: int(x), data)
print (data)
fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
picture = fit.power_law.plot_pdf (color = 'b')
fit.plot_pdf (linewidth = 2, color = 'b', ax = picture)
