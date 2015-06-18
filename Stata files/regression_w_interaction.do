egen Nu1=group(nu1)
egen Nu2=group(nu2)
reg pv_all i.Nu1##i.Nu2
testparm i.Nu2
testparm i.Nu1#i.Nu2

reg pv i.Nu1##i.Nu2
testparm i.Nu1
testparm i.Nu2
testparm i.Nu1#i.Nu2
