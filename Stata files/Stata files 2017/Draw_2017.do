// draw figures one and two

cumul pvc if type == "control", generate(CDF_c_pvc) equal
cumul pvc if type == "treatment" & nu1 == 0, generate(CDF_t_nu1_00_pvc) equal
cumul pvc if type == "treatment" & nu1 < 0.21 & nu1 > .19, generate(CDF_t_nu1_02_pvc) equal
cumul pvc if type == "treatment" & nu1 < 0.41 & nu1 > .39, generate(CDF_t_nu1_04_pvc) equal
cumul pvc if type == "treatment" & nu1 < 0.61 & nu1 > .59, generate(CDF_t_nu1_06_pvc) equal
cumul pvc if type == "treatment" & nu1 < 0.81 & nu1 > .79, generate(CDF_t_nu1_08_pvc) equal
cumul pvc if type == "treatment" & nu1 > .99, generate(CDF_t_nu1_10_pvc) equal

label variable CDF_c_pvc "no onboarding"
label variable CDF_t_nu1_00_pvc "with onboarding, nu1 = 0.0"
label variable CDF_t_nu1_02_pvc "with onboarding, nu1 = 0.2"
label variable CDF_t_nu1_04_pvc "with onboarding, nu1 = 0.4"
label variable CDF_t_nu1_06_pvc "with onboarding, nu1 = 0.6"
label variable CDF_t_nu1_08_pvc "with onboarding, nu1 = 0.8"
label variable CDF_t_nu1_10_pvc "with onboarding, nu1 = 1.0"


twoway (connected CDF_c_pvc pvc, sort msize(tiny)) (connected CDF_t_nu1_00_pvc pvc, sort msize(tiny)) ///
(connected CDF_t_nu1_02_pvc pvc, sort msize(tiny)) (connected CDF_t_nu1_04_pvc pvc, sort msize(tiny)) ///
(connected CDF_t_nu1_06_pvc pvc, sort msize(tiny)) (connected CDF_t_nu1_08_pvc pvc, sort msize(tiny)) ///
(connected CDF_t_nu1_10_pvc pvc, sort msize(tiny)), xline(.1)

cumul pvc if type == "treatment" & nu2 == 0, generate(CDF_t_nu2_00_pvc) equal
cumul pvc if type == "treatment" & nu2 < 0.21 & nu1 > .19, generate(CDF_t_nu2_02_pvc) equal
cumul pvc if type == "treatment" & nu2 < 0.41 & nu1 > .39, generate(CDF_t_nu2_04_pvc) equal
cumul pvc if type == "treatment" & nu2 < 0.61 & nu1 > .59, generate(CDF_t_nu2_06_pvc) equal
cumul pvc if type == "treatment" & nu2 < 0.81 & nu1 > .79, generate(CDF_t_nu2_08_pvc) equal
cumul pvc if type == "treatment" & nu2 > .99, generate(CDF_t_nu2_10_pvc) equal

label variable CDF_c_pvc "no onboarding"
label variable CDF_t_nu2_00_pvc "with onboarding, nu2 = 0.0"
label variable CDF_t_nu2_02_pvc "with onboarding, nu2 = 0.2"
label variable CDF_t_nu2_04_pvc "with onboarding, nu2 = 0.4"
label variable CDF_t_nu2_06_pvc "with onboarding, nu2 = 0.6"
label variable CDF_t_nu2_08_pvc "with onboarding, nu2 = 0.8"
label variable CDF_t_nu2_10_pvc "with onboarding, nu2 = 1.0"

twoway (connected CDF_c_pvc pvc, sort msize(tiny)) (connected CDF_t_nu2_00_pvc pvc, sort msize(tiny)) ///
(connected CDF_t_nu2_02_pvc pvc, sort msize(tiny)) (connected CDF_t_nu2_04_pvc pvc, sort msize(tiny)) ///
(connected CDF_t_nu1_06_pvc pvc, sort msize(tiny)) (connected CDF_t_nu1_08_pvc pvc, sort msize(tiny)) ///
(connected CDF_t_nu2_10_pvc pvc, sort msize(tiny)), xline(.1)

// chart pvalues

histogram pvc, by (type) color(midblue) xline(.1)
histogram pvu, by (type) color(dkgreen) xline(.1)
