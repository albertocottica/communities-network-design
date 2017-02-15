myl = [{'one':'two'},{'three':'four'}]
newl = []


for item in myl:
    newitem ={}
    for key in item:
        newitem[key] = item[key]
        for i in range (3):
            newitem ['fee'] = i
            newl.append(newitem)
            print i
            print newitem
            print newl
