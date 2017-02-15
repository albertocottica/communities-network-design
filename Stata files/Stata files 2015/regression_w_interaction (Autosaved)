egen Nu1=group(nu1)
egen Nu2=group(nu2)
reg pvc i.Nu1##i.Nu2 if type == "treatment"
testparm i.Nu1
testparm i.Nu2
testparm i.Nu1#i.Nu2

reg pvu i.Nu1##i.Nu2
testparm i.Nu1
testparm i.Nu2
testparm i.Nu1#i.Nu2

log using estimation_20170216.smcl
reg x_min i.Nu1##i.Nu2
testparm i.Nu1
testparm i.Nu2
testparm i.Nu1#i.Nu2

reg alphau i.Nu1##i.Nu2
testparm i.Nu1
testparm i.Nu2
testparm i.Nu1#i.Nu2

reg alphac i.Nu1##i.Nu2
testparm i.Nu1
testparm i.Nu2
testparm i.Nu1#i.Nu2

log close

