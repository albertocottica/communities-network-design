egen Nu1=group(nu1)
egen Nu2=group(nu2)
reg pv_all i.Nu1##i.Nu2
testparm i.Nu1
testparm i.Nu2
testparm i.Nu1#i.Nu2

reg pv i.Nu1##i.Nu2
testparm i.Nu1
testparm i.Nu2
testparm i.Nu1#i.Nu2

log using estimation_20150625
reg kmin i.Nu1##i.Nu2
testparm i.Nu1
testparm i.Nu2
testparm i.Nu1#i.Nu2

reg exp_all i.Nu1##i.Nu2
testparm i.Nu1
testparm i.Nu2
testparm i.Nu1#i.Nu2

reg exp i.Nu1##i.Nu2
testparm i.Nu1
testparm i.Nu2
testparm i.Nu1#i.Nu2

log close
translate estimation_20150625.scml estimation_20150625.log
