// remember to load the appropriate data and rename the variables

// p-values

forvalues i = 0.0 (0.2) 1.0 	{
	forvalues j = 0.0 (0.2) 1.0		{
		ttest pvc if nu1 < `i' + .05 & nu1 > `i' - .05 & nu2 > `j' - .05 & nu2 < `j' + .05, by (type)
		// the above is needed because Stata recodes "0.2" as "0.2000001", etc.
		}
	}
	
// kmin

forvalues i = 0.0 (0.2) 1.0 	{
	forvalues j = 0.0 (0.2) 1.0		{
		ttest x_min if nu1 < `i' + .05 & nu1 > `i' - .05 & nu2 > `j' - .05 & nu2 < `j' + .05, by (type)
		// the above is needed because Stata recodes "0.2" as "0.2000001", etc.
		}
	}


// exponents 

forvalues i = 0.0 (0.2) 1.0 	{
	forvalues j = 0.0 (0.2) 1.0		{
		display  `i'
		display  `j'
		ttest alphac if nu1 < `i' + .05 & nu1 > `i' - .05 & nu2 > `j' - .05 & nu2 < `j' + .05, by (type)
		// the above is needed because Stata recodes "0.2" as "0.2000001", etc.
		}
	}
	
	forvalues i = 0.0 (0.2) 1.0 	{
	forvalues j = 0.0 (0.2) 1.0		{
		display  `i'
		display  `j'
		ttest alphau if nu1 < `i' + .05 & nu1 > `i' - .05 & nu2 > `j' - .05 & nu2 < `j' + .05, by (type)
		// the above is needed because Stata recodes "0.2" as "0.2000001", etc.
		}
	}

