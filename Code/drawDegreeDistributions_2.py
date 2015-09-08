# draws degree distributions

# needs a backend for MatPlotLib. I run the code from iPython.
# to do this: copy the code from the script file, then use the cpaste command in iPython
# the object "data" is a list of degrees. Replace your own.

import matplotlib.pyplot as plt
import powerlaw
import json
import os

# insert data here data = []
pathGenerated = '/Users/brenoust/communities-network-design_alberto/Datasets/GeneratedDegrees/'
pathRealData = '/Users/brenoust/communities-network-design_alberto/Datasets/RealWorldDegrees/'

edgeryders = 'Edgeryders_indegree_distribution.csv'
edgerydersData = 'DegreesOfOnBoardingModel_with_onboarding_size_2000_m_1_a_1_alpha_1.000000_gamma_1.000000.json'
innovatoriPA = 'InnovatoriPA_indegree_distribution.csv'
innovatoriPAData = "DegreesOfOnBoardingModel_no_onboarding_size_2000_m_1_a_1_alpha_0.000000_gamma_0.000000.json"
fName = 'DegreesOfOnBoardingModel_with_onboarding_size_2000_m_1_a_1_alpha_0.400000_gamma_0.800000.json'


#plt.xkcd()
#plt.style.use('ggplot')

def displaySaveEach():
	_pathGenerated = '/Users/brenoust/communities-network-design_alberto/Datasets/GeneratedDegrees/'
	_pathRealData = '/Users/brenoust/communities-network-design_alberto/Datasets/RealWorldDegrees/'
	_edgeryders = 'Edgeryders_indegree_distribution.csv'
	_edgerydersData = 'DegreesOfOnBoardingModel_with_onboarding_size_2000_m_1_a_1_alpha_1.000000_gamma_1.000000'
	_innovatoriPA = 'InnovatoriPA_indegree_distribution.csv'
	_innovatoriPAData = "DegreesOfOnBoardingModel_no_onboarding_size_2000_m_1_a_1_alpha_0.000000_gamma_0.000000"
	_resPath = '/Users/brenoust/Google Drive/Sunbelt paper/Code/results/'
	_gPath = '/Users/brenoust/Google Drive/Sunbelt paper/Code/generated/'

	sampleSize = 600

	fList = {}
	associatedFList = {"no onboarding":[], "onboarding 1 1":[]}


	for fName in os.listdir(_resPath):
		if '_it_' in fName:
			dFile = fName.split('_it_')

			nbIt = int(dFile[1].split(".")[0])
			if nbIt >= sampleSize:
				continue

			if _edgerydersData not in fName and _innovatoriPAData not in fName:
				continue

			if dFile[0] not in fList:
				fList[dFile[0]] = []
			fList[dFile[0]].append(fName)

			if _edgerydersData in fName:
				associatedFList["onboarding 1 1"].append(fName)

			if _innovatoriPAData in fName:
				associatedFList["no onboarding"].append(fName)


	#print fList
	associatedData = {"no onboarding":[], "onboarding 1 1":[]}

	for k in associatedData.keys():
		dList = associatedFList[k]
		data = []
		for d in dList:
			fd = open(_resPath + d, 'r')
			dt = json.loads(fd.read())
			data.append(dt)

		associatedData[k] = data

	index = 0
	for d1 in associatedData["no onboarding"]:

		plt.figure(1)
		plt.xlabel('degree')
		plt.ylabel('probability')
		plt.title('Generation with no onboarding')

		fit = powerlaw.Fit (d1, discrete = True, xmin = 1) # creates the fit object
		picture = fit.power_law.plot_pdf (color = 'r', ls='--')
		p = fit.plot_pdf (linewidth = 2, color = 'g', ax = picture)

		fpath = _gPath+"PDF_fit_no_onboarding_"+str(index)+".png"

		plt.savefig(fpath, bbox_inches='tight')
		index += 1
		plt.close()


	plt.figure(2)
	plt.xlabel('degree')
	plt.ylabel('probability')
	plt.title('Innovatori PA')

	f = open(pathRealData + innovatoriPA, 'r')
	data = [float(x.strip()) for x in f.read().split(',')[1:]]
	f.close()
	fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
	picture = fit.power_law.plot_pdf (color = 'r', ls='--')
	p = fit.plot_pdf (linewidth = 2, color = 'g', ax = picture)

	fpath = _gPath+"PDF_fit_innovatoriPA.png"
	plt.savefig(fpath, bbox_inches='tight')
	plt.close()



	#plt.show()

	index = 0
	for d1 in associatedData["onboarding 1 1"]:

		plt.figure(3)
		plt.xlabel('degree')
		plt.ylabel('probability')
		plt.title('Generation with onboarding and pref. att. nu1 = nu2 = 1')

		fit = powerlaw.Fit (d1, discrete = True, xmin = 1) # creates the fit object
		picture = fit.power_law.plot_pdf (color = 'r', ls='--')
		p = fit.plot_pdf (linewidth = 2, color = 'g', ax = picture)

		fpath = _gPath+"PDF_fit_onboarding_nu_1_1__"+str(index)+".png"

		plt.savefig(fpath, bbox_inches='tight')
		index += 1
		plt.close()


	plt.figure(4)
	plt.xlabel('degree')
	plt.ylabel('probability')
	plt.title('Edgeryders')

	f = open(pathRealData + edgeryders, 'r')
	data = [float(x.strip()) for x in f.read().split(',')[1:]]
	f.close()
	fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
	picture = fit.power_law.plot_pdf (color = 'r', ls='--')
	p = fit.plot_pdf (linewidth = 2, color = 'g', ax = picture)

	fpath = _gPath+"PDF_fit_Edgeryders.png"
	plt.savefig(fpath, bbox_inches='tight')
	plt.close()



def concatenateSimulatinOnly():
	_pathGenerated = '/Users/brenoust/communities-network-design_alberto/Datasets/GeneratedDegrees/'
	_pathRealData = '/Users/brenoust/communities-network-design_alberto/Datasets/RealWorldDegrees/'
	_edgeryders = 'Edgeryders_indegree_distribution.csv'
	_edgerydersData = 'DegreesOfOnBoardingModel_with_onboarding_size_2000_m_1_a_1_alpha_1.000000_gamma_1.000000'
	_innovatoriPA = 'InnovatoriPA_indegree_distribution.csv'
	_innovatoriPAData = "DegreesOfOnBoardingModel_no_onboarding_size_2000_m_1_a_1_alpha_0.000000_gamma_0.000000"
	_resPath = '/Users/brenoust/Google Drive/Sunbelt paper/Code/results/'

	sampleSize = 100

	fList = {}
	associatedFList = {"no onboarding":[], "onboarding 1 1":[]}


	for fName in os.listdir(_resPath):
		if '_it_' in fName:
			dFile = fName.split('_it_')

			nbIt = int(dFile[1].split(".")[0])
			if nbIt >= sampleSize:
				continue

			if _edgerydersData not in fName and _innovatoriPAData not in fName:
				continue

			if dFile[0] not in fList:
				fList[dFile[0]] = []
			fList[dFile[0]].append(fName)

			if _edgerydersData in fName:
				associatedFList["onboarding 1 1"].append(fName)

			if _innovatoriPAData in fName:
				associatedFList["no onboarding"].append(fName)


	#print fList
	associatedData = {"no onboarding":[], "onboarding 1 1":[]}

	for k in associatedData.keys():
		dList = associatedFList[k]
		data = []
		for d in dList:
			fd = open(_resPath + d, 'r')
			dt = json.loads(fd.read())
			data.extend(dt)

		associatedData[k] = data


	plt.figure(1)
	plt.xlabel('degree')
	plt.ylabel('probability')
	if (sampleSize>1):
		plt.title('%d generations with no onboarding'%sampleSize)
	else:
		plt.title('Generation with no onboarding')

	d1 = associatedData["no onboarding"]
	fit = powerlaw.Fit (d1, discrete = True, xmin = 1) # creates the fit object
	picture = fit.power_law.plot_pdf (color = 'r', ls='--')
	p = fit.plot_pdf (linewidth = 2, color = 'g', ax = picture)


	plt.figure(2)
	plt.xlabel('degree')
	plt.ylabel('probability')
	plt.title('Innovatori PA')

	f = open(pathRealData + innovatoriPA, 'r')
	data = [float(x.strip()) for x in f.read().split(',')[1:]]
	f.close()
	fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
	picture = fit.power_law.plot_pdf (color = 'r', ls='--')
	p = fit.plot_pdf (linewidth = 2, color = 'g', ax = picture)


	#plt.show()
	plt.figure(3)
	plt.xlabel('degree')
	plt.ylabel('probability')
	if sampleSize > 1:
		plt.title('%d generations with onboarding and pref. att. nu1 = nu2 = 1'%sampleSize)
	else:
		plt.title('Generation with onboarding and pref. att. nu1 = nu2 = 1')


	d1 = associatedData["onboarding 1 1"]
	fit = powerlaw.Fit (d1, discrete = True, xmin = 1) # creates the fit object
	picture = fit.power_law.plot_pdf (color = 'r', ls='--')
	p = fit.plot_pdf (linewidth = 2, color = 'g', ax = picture)

	plt.figure(4)
	plt.xlabel('degree')
	plt.ylabel('probability')
	plt.title('Edgeryders')

	f = open(pathRealData + edgeryders, 'r')
	data = [float(x.strip()) for x in f.read().split(',')[1:]]
	f.close()
	fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
	picture = fit.power_law.plot_pdf (color = 'r', ls='--')
	p = fit.plot_pdf (linewidth = 2, color = 'g', ax = picture)


	plt.show()
	#plt.savefig('foo.png', bbox_inches='tight')



def alternateConcanate():
	_pathGenerated = '/Users/brenoust/communities-network-design_alberto/Datasets/GeneratedDegrees/'
	_pathRealData = '/Users/brenoust/communities-network-design_alberto/Datasets/RealWorldDegrees/'

	_edgeryders = 'Edgeryders_indegree_distribution.csv'
	_edgerydersData = 'DegreesOfOnBoardingModel_with_onboarding_size_2000_m_1_a_1_alpha_1.000000_gamma_1.000000'
	_innovatoriPA = 'InnovatoriPA_indegree_distribution.csv'
	_innovatoriPAData = "DegreesOfOnBoardingModel_no_onboarding_size_2000_m_1_a_1_alpha_0.000000_gamma_0.000000"
	_zeroData = 'DegreesOfOnBoardingModel_with_onboarding_size_2000_m_1_a_1_alpha_0.000000_gamma_0.000000'
	
	_resPath = '/Users/brenoust/Google Drive/Sunbelt paper/Code/results/'

	sampleSize = 600

	fList = {}
	sortedFList = {}
	sortedFList['onboarding'] = {}
	sortedFList['no onboarding'] = []
	#sortedFList['nu2'] = {}


	for fName in os.listdir(_resPath):
		if '_it_' in fName:
			dFile = fName.split('_it_')

			nbIt = int(dFile[1].split(".")[0])
			if nbIt >= sampleSize:
				continue

			if dFile[0] not in fList:
				print dFile[0]
				fList[dFile[0]] = []
			fList[dFile[0]].append(fName)

			if _innovatoriPAData in fName:
				sortedFList['no onboarding'].append(fName)
				continue

			nu2split = dFile[0].split('_gamma_')
			nu2 = float(nu2split[1])
			#if nu2 not in sortedFList['nu2']:
			#	sortedFList['nu2'][nu2] = {}

			nu1split = nu2split[0].split('_alpha_')
			nu1 = float(nu1split[1])
			if nu1 not in sortedFList['onboarding']:
				sortedFList['onboarding'][nu1] = {}

			#if nu1 not in sortedFList['nu2'][nu2]:
			#	sortedFList['nu2'][nu2][nu1] = []
			#sortedFList['nu2'][nu2][nu1].append(fName)

			if nu2 not in sortedFList['onboarding'][nu1]:
				sortedFList['onboarding'][nu1][nu2] = []
			sortedFList['onboarding'][nu1][nu2].append(fName)

	#print fList

	
	f2Data = {}
	for f in fList:
		data = []
		for d in fList[f]:
			fd = open(_resPath + d, 'r')
			dt = json.loads(fd.read())
			data.extend(dt)
		f2Data[f] = data
	
	f2SortedData = {}

	for nu1 in sortedFList['onboarding']:
		f2SortedData[nu1] = {}
		for nu2 in sortedFList['onboarding'][nu1]:
			dList = sortedFList['onboarding'][nu1][nu2]
			f2SortedData[nu1][nu2] = []

			data = []
			for d in dList:
				fd = open(_resPath + d, 'r')
				dt = json.loads(fd.read())
				data.extend(dt)

			f2SortedData[nu1][nu2] = data

	f2NOData = []
	for d in sortedFList['no onboarding']:
		fd = open(_resPath + d, 'r')
		dt = json.loads(fd.read())
		f2NOData.extend(dt)




	plt.figure(1)
	plt.xlabel('degree')
	plt.ylabel('probability')
	plt.title('Edgeryders vs rest')


	fNamePrefix = "DegreesOfOnBoardingModel"


	cvals = []
	colors = plt.get_cmap('Greens', 2*len(f2Data))
	for c in colors(range(len(f2Data))):
		c2 = c
		#c2[3] = .5
		cvals.append(c)

	#print cvals

	index = 0
	for fName in f2Data:
		#if index >= sampleSize:
		#	break

		data = f2Data[fName]

		fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
		#picture = fit.power_law.plot_pdf (color = 'g')
		p = fit.plot_pdf (linewidth = 1, color = cvals[index]) # 'g')#, ax = picture)

		index +=1


	f = open(pathRealData + edgeryders, 'r')
	data = [float(x.strip()) for x in f.read().split(',')[1:]]
	f.close()
	fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
	picture = fit.power_law.plot_pdf (color = 'r', ls='--')
	p = fit.plot_pdf (linewidth = 2, color = 'r', ax = picture)

	data = f2Data[_edgerydersData]
	fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
	picture = fit.power_law.plot_pdf (color = 'g', ls='--')
	p = fit.plot_pdf (linewidth = 2, color = 'g')#, ax = picture)

	data = f2Data[_innovatoriPAData]
	fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
	picture = fit.power_law.plot_pdf (color = 'b', ls='--')
	p = fit.plot_pdf (linewidth = 2, color = 'b')#, ax = picture)

	data = f2Data[_zeroData]
	fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
	picture = fit.power_law.plot_pdf (color = 'o', ls='--')
	p = fit.plot_pdf (linewidth = 2, color = 'o')#, ax = picture)

	#plt.show()
	plt.figure(2)



	cvals = []
	colors = plt.get_cmap('Greens', 2*len(f2Data))
	for c in colors(range(len(f2Data))):
		c2 = c
		#c2[3] = .5
		cvals.append(c)

	
	#fList.reverse()

	index = 0
	for fName in f2Data:
		#if index >= sampleSize:
		#	break
		data = f2Data[fName]

		fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
		#picture = fit.power_law.plot_pdf (color = 'g')
		p = fit.plot_pdf (linewidth = 1, color = cvals[index]) # 'g')#, ax = picture)
		index +=1


	f = open(pathRealData + innovatoriPA, 'r')
	data = [float(x.strip()) for x in f.read().split(',')[1:]]
	f.close()
	fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
	picture = fit.power_law.plot_pdf (color = 'r', ls='--')
	p = fit.plot_pdf (linewidth = 2, color = 'r', ax = picture)


	data = f2Data[_innovatoriPAData]
	fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
	picture = fit.power_law.plot_pdf (color = 'g', ls='--')
	p = fit.plot_pdf (linewidth = 2, color = 'g')#, ax = picture)



	nbCells = len(sortedFList['onboarding'])
	#f, axarr = plt.subplots(len(f2SortedData), len(f2SortedData))

	sortedKeys = sorted(f2SortedData.keys())
	for i in range(len(sortedKeys)):
		u = sortedKeys[i]
		plt.figure(3+i)

		plt.xlabel('degree')
		plt.ylabel('probability')
		plt.title('nu1 = %3f'%u)

	
		print i, " ", u
		for j in range(len(sortedKeys)):
			v = sortedKeys[j]
			print j, ' ',v
		
			data = f2SortedData[u][v]

			fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
			p = fit.plot_pdf (linewidth = 1, color = cvals[len(cvals)-1]) # 'g')#, ax = picture)

			data = f2Data[_innovatoriPAData]
			fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
			#picture = fit.power_law.plot_pdf (color = 'b', ls='--')
			p = fit.plot_pdf (linewidth = 1, color = 'r', ls='--')#, ax = picture)



	for i in range(len(sortedKeys)):
		u = sortedKeys[i]
		plt.figure(3+len(sortedKeys)+i)

		plt.xlabel('degree')
		plt.ylabel('probability')
		plt.title('nu2 = %3f'%u)
	
		print i, " ", u
		for j in range(len(sortedKeys)):
			v = sortedKeys[j]
			print j, ' ',v
		
			data = f2SortedData[v][u]

			fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
			p = fit.plot_pdf (linewidth = 1, color = cvals[len(cvals)-1]) # 'g')#, ax = picture)

			data = f2Data[_innovatoriPAData]
			fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
			#picture = fit.power_law.plot_pdf (color = 'b', ls='--')
			p = fit.plot_pdf (linewidth = 1, color = 'r', ls='--')#, ax = picture)



	plt.figure(3+2*len(sortedKeys)+1)
	plt.xlabel('degree')
	plt.ylabel('probability')
	
	data = f2Data[_edgerydersData]
	fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
	#picture = fit.power_law.plot_pdf (color = 'r', ls='--')
	p = fit.plot_pdf (linewidth = 1, color = 'g', ls='--')#, ax = picture)

	data = f2Data[_zeroData]
	fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
	#picture = fit.power_law.plot_pdf (color = 'g', ls='--')
	p = fit.plot_pdf (linewidth = 1, color = 'b', ls='--')#, ax = picture)

	data = f2Data[_innovatoriPAData]
	fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
	#picture = fit.power_law.plot_pdf (color = 'b', ls='--')
	p = fit.plot_pdf (linewidth = 1, color = 'r', ls='--')#, ax = picture)
	


	plt.figure(3+2*len(sortedKeys)+2)
	plt.xlabel('degree')
	plt.ylabel('probability')
	plt.title('comparison of the generated networks')

	for fName in f2Data:
		#if index >= sampleSize:
		#	break
		if fName in [_innovatoriPAData, _edgerydersData, _zeroData]:
			print "SKIP ",fName
			continue

		data = f2Data[fName]

		fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
		#picture = fit.power_law.plot_pdf (color = 'g')
		p = fit.plot_pdf (linewidth = 1, color = cvals[15]) # 'g')#, ax = picture)
		index +=1

	
	data = f2Data[_edgerydersData]
	fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
	#picture = fit.power_law.plot_pdf (color = 'r', ls='--')
	p = fit.plot_pdf (linewidth = 2, color = 'g', ls='--')#, ax = picture)

	data = f2Data[_zeroData]
	fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
	#picture = fit.power_law.plot_pdf (color = 'g', ls='--')
	p = fit.plot_pdf (linewidth = 2, color = 'b', ls='--')#, ax = picture)

	data = f2Data[_innovatoriPAData]
	fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
	#picture = fit.power_law.plot_pdf (color = 'b', ls='--')
	p = fit.plot_pdf (linewidth = 2, color = 'r', ls='--')#, ax = picture)



	plt.show()




def plotCompareRealGeneratedEdgeryders():

	plt.figure(1)


	fNamePrefix = "DegreesOfOnBoardingModel"


	fList = []
	for fName in os.listdir(pathGenerated):
		if fNamePrefix in fName:
			fList.append(fName)

	cvals = []
	colors = plt.get_cmap('Greens', 2*len(fList))
	for c in colors(range(len(fList))):
		c2 = c
		#c2[3] = .5
		cvals.append(c)

	#print cvals

	index = 0
	for fName in fList:
		f = open(pathGenerated + fName, 'r')
		data = json.loads(f.read())

		fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
		#picture = fit.power_law.plot_pdf (color = 'g')
		p = fit.plot_pdf (linewidth = 1, color = cvals[index]) # 'g')#, ax = picture)
		index +=1


	f = open(pathRealData + edgeryders, 'r')
	data = [float(x.strip()) for x in f.read().split(',')[1:]]
	f.close()
	fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
	picture = fit.power_law.plot_pdf (color = 'r', ls='--')
	p = fit.plot_pdf (linewidth = 2, color = 'r', ax = picture)

	f = open(pathGenerated + edgerydersData, 'r')
	data = json.loads(f.read())
	f.close()
	fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
	picture = fit.power_law.plot_pdf (color = 'g', ls='--')
	p = fit.plot_pdf (linewidth = 2, color = 'g')#, ax = picture)


	#plt.show()


def plotCompareRealGeneratedInnovatoriPA():

	plt.figure(2)


	fNamePrefix = "DegreesOfOnBoardingModel"


	fList = []
	for fName in os.listdir(pathGenerated):
		if fNamePrefix in fName:
			fList.append(fName)

	cvals = []
	colors = plt.get_cmap('Greens', 2*len(fList))
	for c in colors(range(len(fList))):
		c2 = c
		#c2[3] = .5
		cvals.append(c)

	#print cvals
	fList.reverse()

	index = 0
	for fName in fList:
		f = open(pathGenerated + fName, 'r')
		data = json.loads(f.read())

		fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
		#picture = fit.power_law.plot_pdf (color = 'g')
		p = fit.plot_pdf (linewidth = 1, color = cvals[index]) # 'g')#, ax = picture)
		index +=1


	f = open(pathRealData + innovatoriPA, 'r')
	data = [float(x.strip()) for x in f.read().split(',')[1:]]
	f.close()
	fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
	picture = fit.power_law.plot_pdf (color = 'r', ls='--')
	p = fit.plot_pdf (linewidth = 2, color = 'r', ax = picture)

	f = open(pathGenerated + innovatoriPAData, 'r')
	data = json.loads(f.read())
	f.close()
	fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
	picture = fit.power_law.plot_pdf (color = 'g', ls='--')
	p = fit.plot_pdf (linewidth = 2, color = 'g')#, ax = picture)


	plt.show()




def plotAllDistributions():

	plt.figure(1)

	fNamePrefix = "DegreesOfOnBoardingModel"
	for fName in os.listdir(pathGenerated):
		if fNamePrefix in fName:

			f = open(pathGenerated + fName, 'r')
			data = json.loads(f.read())

			fit = powerlaw.Fit (data, discrete = True, xmin = 1) # creates the fit object
			picture = fit.power_law.plot_pdf (color = 'b')
			p = fit.plot_pdf (linewidth = 2, color = 'r', ax = picture)

	plt.show()

#displaySaveEach()
#concatenateSimulatinOnly()
alternateConcanate()
#plotAllDistributions()

#plotCompareRealGeneratedEdgeryders()
#plotCompareRealGeneratedInnovatoriPA()
exit(0)


