# Simulates the interaction network in a growing online community with onboarding policy
# The network is directed
import networkx
import random
import time
import powerlaw
from multiprocessing import Pool

class OnBoardingModel(object):
	"""docstring for CotticaModel"""
	def __init__(self, m, networkSize, alpha, gamma):
		super(OnBoardingModel, self).__init__()

		self.graph = networkx.MultiDiGraph()

		# model parameters
		self.m = m # the number of preferential attachment edges to be added at each step
		self.networkSize = networkSize
		self.alpha = alpha # prob that newcomer follows the manager advice and reach out to someone else
		self.gamma = gamma 

		# recording timestep for convenience, so the evolution of the network can be animated if needed
		self.timestepProp = None
		self.time_step = 0

		self.newly_added_node = None
		self.current_node_index = 0
		self.current_edge_index = 0

	def __initialize__(self):
		'''
		start with two reciprocally connected nodes 
		'''
		node1 = self.current_node_index
		self.graph.add_node(self.current_node_index, {'time_step': self.time_step, 'a': 1.0})
		self.newly_added_node = self.current_node_index

		self.time_step += 1
		self.current_node_index += 1
		node2 = self.current_node_index
		self.graph.add_node(self.current_node_index, {'time_step': self.time_step, 'a': 1.0})
		self.newly_added_node = self.current_node_index

		self.time_step += 1
		self.graph.add_edge(node1, node2, self.current_edge_index, {'time_step': self.time_step})
		
		self.time_step += 1
		self.current_edge_index += 1
		self.graph.add_edge(node2, node1, self.current_edge_index, {'time_step': self.time_step})

	def __addOneNode__(self):
		'''
		At each timestep, one node joins.
		The newly created node is stored as the newly added node for convenience
		'''
		self.time_step += 1
		self.current_node_index += 1
		# value a could be set using a function and be different for each node
		node = self.graph.add_node(self.current_node_index, {'time_step': self.time_step, 'a': 1.0})
		self.newly_added_node = self.current_node_index

	def __selectUniform__(self):
		return self.graph.nodes()[random.randint(0, self.current_node_index)]

	def __selectFromInDeg__(self):
		'''
		nodes are chosen with probability proportional to their deg + m * a
		where a is a node value stored in a metric property
		'''
		nodes = self.graph.nodes(True) # list of couples (node, property dict {'time_step', 'a'}) as stored on node creation
		in_degrees = map(lambda x: self.graph.in_degree(x[0]), nodes) # array of nodes in_degree

		# zip nodes, dict and in_degree into a single list [[node, dict], in_degree]
		# compute for each node the value: in_degree + a
		# sum up all these values

		# x is an entry [[node, dict], in_degree] in the zipped list
		# x[1] is in_degree
		# x[0][1] is a dict {'time_step', 'a'}
		sumValues = sum(map(lambda x: x[1] + self.m * x[0][1]['a'], zip(nodes, in_degrees))) 
		
		threshold = random.random() * sumValues # draw a number at random
		s = 0 # go fetch the node that this number implicitly points to
		for node in self.graph.nodes():
			s += in_degrees[node] + self.m * nodes[node][1]['a']
			if s >= threshold:
				return node
		
	def __preferentialAttachmentEdges__(self):
		'''
		At each timestep add m (small number, possibly 1 or 2) edges.
		'''
		for i in range(self.m):
			'''		
			- edge source is randomly allocated
			- edge target is selected with probability proportional to nodes in-degree.
			- this is "pure" preferential attachment; does not take into account "chattiness", that
			  would allocate targets taking into account out-degree too. This can be changed later
			'''
			source = self.__selectUniform__()
			target = self.__selectFromInDeg__()
			while source == target:
				target = self.__selectFromInDeg__()

			self.time_step += 1
			self.current_edge_index += 1
			self.graph.add_edge(source, target, self.current_edge_index, {'time_step': self.time_step})


	def __onboarding__(self):
		'''
		- At each timestep, one edge is directed to the new node.
		--> that does not say how source is selected, let's agree to select uniformly
		'''
		source = self.__selectUniform__()
		while source == self.newly_added_node:
			source = self.__selectUniform__()

		self.time_step += 1
		self.current_edge_index += 1
		self.graph.add_edge(source, self.newly_added_node, self.current_edge_index, {'time_step': self.time_step})
		
		'''
		- With probability alpha, "the new community members reacts": one edge is added with the new 
		  node as source. The target is allocated by preferential attachment.
		'''
		if self.alpha > random.random():
			target = self.__selectFromInDeg__()
			while target == self.newly_added_node:
				target = self.__selectFromInDeg__()

			self.time_step += 1
			self.current_edge_index += 1
			self.graph.add_edge(self.newly_added_node, target, self.current_edge_index, {'time_step': self.time_step})

		'''
		- With probability gamma, "onboarding works": one edge is added with the new node as target
		  and a randomly chosen source.
		'''
		if self.gamma > random.random():
			source = self.__selectUniform__()
			while source == self.newly_added_node:
				source = self.__selectUniform__()

				self.time_step += 1
				self.current_edge_index += 1
				self.graph.add_edge(source, self.newly_added_node, self.current_edge_index, {'time_step': self.time_step})

	def generate(self, onboarding = True):
		'''
		Generates a new graph according to Cottica model
		each time this routine is called
		Note: self.graph must be stored to disk (using tlp.saveGraph())
		if previous generation process should be saved.
		'''

		self.__initialize__()
		for t in range(self.networkSize):
			self.__addOneNode__()
			self.__preferentialAttachmentEdges__()
			if onboarding:
				self.__onboarding__()

	def get_degree_distribution(self):
		'''
		Returns a (non sorted) list, each element of which is the degree of one node of graph.
		'''
		return [self.graph.in_degree(node) for node in self.graph.nodes_iter()]

class PowerlawFitting(object):
	"""docstring for PowerlawFitting"""
	def __init__(self, degree_distribution, nb_runs):
		super(PowerlawFitting, self).__init__()
		self.degree_distribution = degree_distribution
		self.network_size = len(self.degree_distribution)
		self.nb_runs = nb_runs

		# declare internal fields initialized with stub values
		self.fit = None
		self.alpha = 0.0
		self.D = 0.0
		self.xmin = 1.0 # we suspect the 'optimal' xmin to be greater than 1.0
		self.p_value = 0.0

		# the associated '_all' fields correspond to a xmin of 1.0
		self.fit_all = None
		self.alpha_all = 0.0
		self.D_all = 0.0
		self.p_value_all = 0.0

	
	def fit_to_powerLaw(self):
		'''
		Note: dd stands for self.degree_distribution
		list => {'alphaAll':float, 'pvalueAll': float, 'alpha':float, 'pvalue':pvalue, 'xmin':xmin}
		Runs a goodness-of-fit test of the degree distribution dd to a power law.
		Null hypothesis: dd was generated by a power law + randomness
		
		Computes the following five values:
		1. alpha_all: an estimate for the exponent of the power function, fitted onto the whole distribution.
		2. pvalue_all: the probability that the observed data were generated by a power law with exponent alphaAll. The null is rejected for pvalueAll < 0.1.
		3. alpha: an estimate for the exponent of the power function, fitted onto the distribution's upper tail x >= xmin.
		4. pvalue: the probability that the observed data were generated by a power law with exponent alpha. The null is rejected for pvalue < 0.1.
		5. xmin: the value of xmin that minizes the D statistic. 

		Note : test based on Clauset et al. (2009)
		'''

		# we fit this degree distribution to a power law
		# the fitting routine uses a xmin value that minimizes
		# the distance of the given distribution to the fitted curve
		self.fit = powerlaw.Fit(self.degree_distribution, discrete = True) # creates the Fit object
		self.alpha = self.fit.power_law.alpha
		self.D = self.fit.power_law.D
		self.xmin = self.fit.power_law.xmin

		# we also compute the distance when taking the whole distribution
		# (that is, when forcing xmin = 0)

		self.fit_all = powerlaw.Fit(self.degree_distribution, discrete = True, xmin = 1.0) # creates a Fit object whil imposing the power law on the whole support 
		self.alpha_all = self.fit_all.power_law.alpha
		self.D_all = self.fit_all.power_law.D

		# compute p_value for optimal xmin value
		synth_more_distant = 0
		for j in range (self.nb_runs): # corresponds to an estimate of p-value accurate to the second decimal point when nb_runs = 2500
			synthData = self.__generate_synthetic_data__ (self.fit)
			synthFit = powerlaw.Fit(synthData, discrete = True)
			synthD = synthFit.power_law.D
			if synthD > self.D:
				synth_more_distant += 1
		self.p_value = float(synth_more_distant) / self.nb_runs

		# compute p_value for whole distribution, that is force xmin = 1
		synth_more_distant = 0
		for j in range (self.nb_runs): # corresponds to an estimate of p-value accurate to the second decimal point when nb_runs = 2500
			synthData = self.__generate_synthetic_data__(self.fit_all)
			synthFit = powerlaw.Fit(synthData, discrete = True)
			synthD = synthFit.power_law.D
			if synthD > self.D_all:
				synth_more_distant += 1
		self.p_value_all = float(synth_more_distant) / self.nb_runs


	def __generate_synthetic_data__(self, fit_object): # n, nTail):
		# Note: the fit object knows about its xmin value

		# count how many nodes have a degree above or equal to xmin
		# this is stored in nTail
		nTail = sum(map(lambda x: 1 if x >= fit_object.xmin else 0, self.degree_distribution))

		# additionally store the list of degrees (nodes) below xmin
		lowerTail = [x for x in self.degree_distribution if x < fit_object.xmin]

		nTail = 0
		lowerTail = []
		for x in self.degree_distribution:
			if x >= fit_object.xmin:
				nTail += 1
			else:
				lowerTail.append(x)



		# synthetic data is obtained using the following trick.
		# observation: there is probability p = nTail/self.network_size that a node is part of the end tail
		# toss a coin with probability p of success
		# if so use the fitted distribution to generate a node (its degree) part of the tail at random
		# if not draw a value at random from lowerTail
		synthData = []
		for j in range (self.network_size):
			generated_value = None
			if random.random() < float(nTail)/networkSize:
				generated_value = fit_object.power_law.generate_random(1)
			else: 
				generated_value = random.sample(lowerTail, 1)

			synthData.append(float(generated_value[0]))

		return synthData



'''
the next function is defined as external to the above classes
to make it easier to call them from the multiprocessing package
'''
def generate_and_fit_network(input_tuple, onboarding = True):

	# input_tuple contains [m, networkSize, alpha, gamma, nb_runs] to feed the on-boarding model
	# plus the number of runs used to compute p_values
	m = input_tuple[0]
	networkSize =input_tuple[1]
	alpha = input_tuple[2]
	gamma = input_tuple[3]
	nb_runs = input_tuple[4]

	cm = OnBoardingModel(m, networkSize, alpha, gamma)
	cm.generate(onboarding)
	degree_distribution = cm.get_degree_distribution()

	pf = PowerlawFitting(degree_distribution, nb_runs)
	pf.fit_to_powerLaw()
	return [pf.alpha_all, pf.p_value_all, pf.alpha, pf.p_value, pf.xmin]


if __name__ == '__main__':

	# Initialization
	m = 2
	networkSize = 2000 # nb steps to iterate node addition, pref attach and on-boarding
	#alpha = 0.75
	#gamma = 0.6

	alphas = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
	gammas = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
	onboarding = True
	nb_runs = 2500

	#path = '/Users/melancon/Documents/Recherche/Work in progress/Alberto/' # change this to your local path
	path = '/net/cremi/gmelanco/Alberto/' # change this to your local path
	global_start = time.time()

	for alpha in alphas:
		for gamma in gammas:

			filename = 'Fitting_statistics_' +  str(networkSize)  + '_' + str(m) + '_' + str(onboarding) + '_' + str(alpha) + '_' + str(gamma) + '_' + str(nb_runs) + '.txt'# use a name with m and networkSize and trial number

			print 'Dealing with alpha, gamma = ' + str(alpha) + ', ' + str(gamma)
			print '\tSet all variables'

			# Real work starts here
			start = time.time()

			# number of workers is number of processes ran in parallel
			# this should ultimately be equal to the number of networks we wish to generate
			nb_workers = 100
			# builds an input_tuple fro each of the processes
			input_tuples = [[m, networkSize, alpha, gamma, nb_runs] for graphNameIndex in range(nb_workers)]
			print '\tBuilt tuples'
			print input_tuples
			print '\t*********************************'
			# processes are launched, the multiprocessing package takes care of dispatching things around
			p = Pool(nb_workers)

			all_stats = p.map(generate_and_fit_network, input_tuples, onboarding)
			#stats = generate_and_fit_network(input_tuples[0])

			fp = open(path + filename, 'w')
			fp.write('\n'.join(map(lambda x: str(x), all_stats)))
			fp.close()
			print '\tDealing with alpha, gamma = ' + str(alpha) + ', ' + str(gamma) + ' took ', time.time()-start, ' seconds'
	#print all_stats
	#print stats

	print 'The whole thing took ', time.time()-global_start, ' seconds'
