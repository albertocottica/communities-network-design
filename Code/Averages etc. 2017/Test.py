myl = [{'one':'two'}, {'five':'six'}]
newl = []

for i in range (2):
    print ( 'i = ' + str(i))
    for item in myl:
        newItem = {}
        print ('item = ' + str (item))
        for key in item:
            newItem[key] = item[key]
            newItem['fee'] = i
            print ('newItem = ' + str (newItem))
        newl.append(newItem)
    print newl
        