// draw graphs in figure 3

cumul pvc if type == "control" & nu1 == 0 & nu2 == 0, generate(CDF_c_pvc) equal
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


twoway (connected CDF_c_pvc pvc, sort msize(small)) (connected CDF_t_nu1_00_pvc pvc, sort msize(tiny)) ///
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

twoway (connected CDF_c_pvc pvc, sort msize(small)) (connected CDF_t_nu2_00_pvc pvc, sort msize(tiny)) ///
(connected CDF_t_nu2_02_pvc pvc, sort msize(tiny)) (connected CDF_t_nu2_04_pvc pvc, sort msize(tiny)) ///
(connected CDF_t_nu2_06_pvc pvc, sort msize(tiny)) (connected CDF_t_nu2_08_pvc pvc, sort msize(tiny)) ///
(connected CDF_t_nu2_10_pvc pvc, sort msize(tiny)), xline(.1)

// chart pvalues

histogram pvc, by (type) color(midblue) xline(.1)
histogram pvu, by (type) color(dkgreen) xline(.1)

// draw graphs in figure 4

gen kmin = x_min - 1

// the above is because x_min refers to q = k + ma


cumul kmin if type == "control" & nu1 == 0 & nu2 == 0, generate(CDF_c_kmin) equal
cumul kmin if type == "treatment" & nu1 == 0, generate(CDF_t_nu1_00_kmin) equal
cumul kmin if type == "treatment" & nu1 < 0.21 & nu1 > .19, generate(CDF_t_nu1_02_kmin) equal
cumul kmin if type == "treatment" & nu1 < 0.41 & nu1 > .39, generate(CDF_t_nu1_04_kmin) equal
cumul kmin if type == "treatment" & nu1 < 0.61 & nu1 > .59, generate(CDF_t_nu1_06_kmin) equal
cumul kmin if type == "treatment" & nu1 < 0.81 & nu1 > .79, generate(CDF_t_nu1_08_kmin) equal
cumul kmin if type == "treatment" & nu1 > .99, generate(CDF_t_nu1_10_kmin) equal

label variable CDF_c_kmin "no onboarding"
label variable CDF_t_nu1_00_kmin "with onboarding, nu1 = 0.0"
label variable CDF_t_nu1_02_kmin "with onboarding, nu1 = 0.2"
label variable CDF_t_nu1_04_kmin "with onboarding, nu1 = 0.4"
label variable CDF_t_nu1_06_kmin "with onboarding, nu1 = 0.6"
label variable CDF_t_nu1_08_kmin "with onboarding, nu1 = 0.8"
label variable CDF_t_nu1_10_kmin "with onboarding, nu1 = 1.0"

twoway (connected CDF_c_kmin kmin, sort msize(small)) (connected CDF_t_nu1_00_kmin kmin, sort msize(tiny)) ///
(connected CDF_t_nu1_02_kmin kmin, sort msize(tiny)) (connected CDF_t_nu1_04_kmin kmin, sort msize(tiny)) ///
(connected CDF_t_nu1_06_kmin kmin, sort msize(tiny)) (connected CDF_t_nu1_08_kmin kmin, sort msize(tiny)) ///
(connected CDF_t_nu1_10_kmin kmin, sort msize(tiny)), xline(2)

//


cumul kmin if type == "treatment" & nu2 == 0, generate(CDF_t_nu2_00_kmin) equal
cumul kmin if type == "treatment" & nu2 < 0.21 & nu2 > .19, generate(CDF_t_nu2_02_kmin) equal
cumul kmin if type == "treatment" & nu2 < 0.41 & nu2 > .39, generate(CDF_t_nu2_04_kmin) equal
cumul kmin if type == "treatment" & nu2 < 0.61 & nu2 > .59, generate(CDF_t_nu2_06_kmin) equal
cumul kmin if type == "treatment" & nu2 < 0.81 & nu2 > .79, generate(CDF_t_nu2_08_kmin) equal
cumul kmin if type == "treatment" & nu2 > .99, generate(CDF_t_nu2_10_kmin) equal

label variable CDF_c_kmin "no onboarding"
label variable CDF_t_nu2_00_kmin "with onboarding, nu2 = 0.0"
label variable CDF_t_nu2_02_kmin "with onboarding, nu2 = 0.2"
label variable CDF_t_nu2_04_kmin "with onboarding, nu2 = 0.4"
label variable CDF_t_nu2_06_kmin "with onboarding, nu2 = 0.6"
label variable CDF_t_nu2_08_kmin "with onboarding, nu2 = 0.8"
label variable CDF_t_nu2_10_kmin "with onboarding, nu2 = 1.0"

twoway (connected CDF_c_kmin kmin, sort msize(small)) (connected CDF_t_nu2_00_kmin kmin, sort msize(tiny)) ///
(connected CDF_t_nu2_02_kmin kmin, sort msize(tiny)) (connected CDF_t_nu2_04_kmin kmin, sort msize(tiny)) ///
(connected CDF_t_nu2_06_kmin kmin, sort msize(tiny)) (connected CDF_t_nu2_08_kmin kmin, sort msize(tiny)) ///
(connected CDF_t_nu2_10_kmin kmin, sort msize(tiny)), xline(2)


// tentative graphs for Revision July 2017

// grouping on nu1

cumul pvu if type == "control" & nu1 == 0 & nu2 == 0, generate(CDF_c_pvu) equal
cumul pvu if type == "treatment" & nu1 == 0, generate(CDF_t_nu1_00_pvu) equal
cumul pvu if type == "treatment" & nu1 < 0.21 & nu1 > .19, generate(CDF_t_nu1_02_pvu) equal
cumul pvu if type == "treatment" & nu1 < 0.41 & nu1 > .39, generate(CDF_t_nu1_04_pvu) equal
cumul pvu if type == "treatment" & nu1 < 0.61 & nu1 > .59, generate(CDF_t_nu1_06_pvu) equal
cumul pvu if type == "treatment" & nu1 < 0.81 & nu1 > .79, generate(CDF_t_nu1_08_pvu) equal
cumul pvu if type == "treatment" & nu1 > .99, generate(CDF_t_nu1_10_pvu) equal

label variable CDF_c_pvu "no onboarding"
label variable CDF_t_nu1_00_pvu "with onboarding, nu1 = 0.0"
label variable CDF_t_nu1_02_pvu "with onboarding, nu1 = 0.2"
label variable CDF_t_nu1_04_pvu "with onboarding, nu1 = 0.4"
label variable CDF_t_nu1_06_pvu "with onboarding, nu1 = 0.6"
label variable CDF_t_nu1_08_pvu "with onboarding, nu1 = 0.8"
label variable CDF_t_nu1_10_pvu "with onboarding, nu1 = 1.0"


twoway (connected CDF_c_pvu pvu, sort msize(small)) (connected CDF_t_nu1_00_pvu pvu, sort msize(tiny)) ///
(connected CDF_t_nu1_02_pvu pvu, sort msize(tiny)) (connected CDF_t_nu1_04_pvu pvu, sort msize(tiny)) ///
(connected CDF_t_nu1_06_pvu pvu, sort msize(tiny)) (connected CDF_t_nu1_08_pvu pvu, sort msize(tiny)) ///
(connected CDF_t_nu1_10_pvu pvu, sort msize(tiny)), xline(.1)

// grouping on nu2

cumul pvu if type == "treatment" & nu2 == 0, generate(CDF_t_nu2_00_pvu) equal
cumul pvu if type == "treatment" & nu2 < 0.21 & nu1 > .19, generate(CDF_t_nu2_02_pvu) equal
cumul pvu if type == "treatment" & nu2 < 0.41 & nu1 > .39, generate(CDF_t_nu2_04_pvu) equal
cumul pvu if type == "treatment" & nu2 < 0.61 & nu1 > .59, generate(CDF_t_nu2_06_pvu) equal
cumul pvu if type == "treatment" & nu2 < 0.81 & nu1 > .79, generate(CDF_t_nu2_08_pvu) equal
cumul pvu if type == "treatment" & nu2 > .99, generate(CDF_t_nu2_10_pvu) equal

label variable CDF_c_pvu "no onboarding"
label variable CDF_t_nu2_00_pvu "with onboarding, nu2 = 0.0"
label variable CDF_t_nu2_02_pvu "with onboarding, nu2 = 0.2"
label variable CDF_t_nu2_04_pvu "with onboarding, nu2 = 0.4"
label variable CDF_t_nu2_06_pvu "with onboarding, nu2 = 0.6"
label variable CDF_t_nu2_08_pvu "with onboarding, nu2 = 0.8"
label variable CDF_t_nu2_10_pvu "with onboarding, nu2 = 1.0"

twoway (connected CDF_c_pvu pvu, sort msize(small)) (connected CDF_t_nu2_00_pvu pvu, sort msize(tiny)) ///
(connected CDF_t_nu2_02_pvu pvu, sort msize(tiny)) (connected CDF_t_nu2_04_pvu pvu, sort msize(tiny)) ///
(connected CDF_t_nu2_06_pvu pvu, sort msize(tiny)) (connected CDF_t_nu2_08_pvu pvu, sort msize(tiny)) ///
(connected CDF_t_nu2_10_pvu pvu, sort msize(tiny)), xline(.1)



