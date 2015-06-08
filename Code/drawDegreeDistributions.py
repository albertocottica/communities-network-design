# draws degree distributions

# needs a backend for MatPlotLib. I run the code from iPython.
# to do this: copy the code from the script file, then use the cpaste command in iPython
# the object "data" is a list of degrees. Replace your own.

import powerlaw

data = [0.0, 1.0, 10.0, 3.0, 0.0, 1.0, 1.0, 4.0]

fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
picture = fit.power_law.plot_pdf (color = 'b')
fit.plot_pdf (linewidth = 2, color = 'b', ax = picture)
