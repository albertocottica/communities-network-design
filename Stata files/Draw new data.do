cumul pv_all if ob == 0, generate(CDF_f_pv_all) equal
cumul pv_all if ob == 1 & nu1 == 0, generate(CDF_nu1_00_pv_all) equal
cumul pv_all if ob == 1 & nu1 < 0.21 & nu1 > .19, generate(CDF_nu1_02_pv_all) equal
cumul pv_all if ob == 1 & nu1 < 0.41 & nu1 > .39, generate(CDF_nu1_04_pv_all) equal
cumul pv_all if ob == 1 & nu1 < .61 & nu1 > .59, generate(CDF_nu1_06_pv_all) equal
cumul pv_all if ob == 1 & nu1 < .81 & nu1 > .79, generate(CDF_nu1_08_pv_all) equal
cumul pv_all if ob == 1 & nu1 == 1, generate(CDF_nu1_10_pv_all) equal

twoway (connected CDF_f_pv_all pv_all, sort) (connected CDF_nu1_00_pv_all pv_all, sort) ///
(connected CDF_nu1_02_pv_all pv_all, sort) (connected CDF_nu1_04_pv_all pv_all, sort) ///
(connected CDF_nu1_06_pv_all pv_all, sort) (connected CDF_nu1_08_pv_all pv_all, sort) ///
(connected CDF_nu1_10_pv_all pv_all, sort), xline(.1)
