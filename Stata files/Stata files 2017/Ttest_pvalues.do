use "/Users/albertocottica/github/local/communities-network-design/Stata files/Stata files 2017/data4Stata.dta"


forvalues i = 0.0 (0.2) 1.0 	{
	forvalues j = 0.0 (0.2) 1.0		{
		ttest pvc if nu1 < `i' + .05 & nu1 > `i' - .05 & nu2 > `j' - .05 & nu2 < `j' + .05, by (type)
		// the above is needed because Stata recodes "0.2" as "0.2000001", etc.
		}
	}
	
