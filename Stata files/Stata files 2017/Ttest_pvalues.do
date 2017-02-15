use "/Users/albertocottica/github/local/communities-network-design/Stata files/Stata files 2017/data4Stata.dta"

rename p_value pvu
rename p_value_constrained pvc

forvalues i = 0.0 (0.2) 1.0 	{
	forvalues j = 0.0 (0.2) 1.0		{
		ttest pvc if nu1 == `i' & nu2 == `j', by (type)
		}
	}
	
