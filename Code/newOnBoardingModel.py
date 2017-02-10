# Simulates the interaction network in a growing online community with onboarding policy
# The network is directed
import networkx
import random as rd
import time
import powerlaw_c as powerlaw
import math
from multiprocessing import Pool


import time                                                

# time profiler decorator
def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te-ts)
        return result

    return timed


class OnBoardingModel(object):
    """docstring for CotticaModel"""
    def __init__(self, m, a, networkSize, nu1, nu2, onBoard):
        super(OnBoardingModel, self).__init__()

        self.graph = networkx.MultiDiGraph()

        # model parameters
        self.m = m
        self.a = a
        self.networkSize = networkSize
        self.nu1 = nu1 # prob that newcomer follows the manager advice and reach out to someone else
        self.nu2 = nu2
        self.onBoard = onBoard

        # recording timestep for convenience, so the evolution of the network can be animated if needed
        self.timestepProp = None
        self.time_step = 0

        self.newly_added_node = None
        self.current_node_index = 0
        self.current_edge_index = 0

        self.tulip_node_ids = []
        self.numberOfNodes = 0

    def __initialize__(self):
        '''
        start with two reciprocally connected nodes
        '''
        node1 = self.current_node_index
        self.graph.add_node(self.current_node_index, {'time_step': self.time_step, 'a': self.a})
        self.newly_added_node = self.current_node_index

        self.time_step += 1
        self.current_node_index += 1
        node2 = self.current_node_index
        self.graph.add_node(self.current_node_index, {'time_step': self.time_step, 'a': self.a})
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
        node = self.graph.add_node(self.current_node_index, {'time_step': self.time_step, 'a': self.a})
        self.newly_added_node = self.current_node_index
        self.numberOfNodes += 1




    def __selectUniform__(self):
        return self.graph.nodes()[rd.randint(0, self.current_node_index)]


    def __selectFromInDeg__(self):
        '''
        nodes are chosen with probability proportional to their deg + m * a
        where a is a node value stored in a metric property
        '''
        nodes = self.graph.nodes(True) # couples (node, property dict)
        in_degrees = map(lambda x: self.graph.in_degree(x[0]), nodes)

        sumValues = sum(map(lambda x: x[1] + self.m * x[0][1]['a'], zip(nodes, in_degrees))) # I don't get this. Why apply lambda (function of ONE variable) to pairs of values in zip?
        threshold = rd.random() * sumValues
        s = 0
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
        - With probability nu1, "the new community members reacts": one edge is added with the new
          node as source. The target is allocated by preferential attachment.
        '''
        if self.nu1 > rd.random():
            target = self.__selectFromInDeg__()
            while target == self.newly_added_node:
                target = self.__selectFromInDeg__()

            self.time_step += 1
            self.current_edge_index += 1
            self.graph.add_edge(self.newly_added_node, target, self.current_edge_index, {'time_step': self.time_step})

        '''
        - With probability nu2, "onboarding works": one edge is added with the new node as target
          and a randomly chosen source.
        '''
        if self.nu2 > rd.random():
            source = self.__selectUniform__()
            while source == self.newly_added_node:
                source = self.__selectUniform__()

                self.time_step += 1
                self.current_edge_index += 1
                self.graph.add_edge(source, self.newly_added_node, self.current_edge_index, {'time_step': self.time_step})



    def generate(self):
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
            if self.onBoard == True:
                self.__onboarding__()


    def get_raw_degree_distribution(self):
        '''
        Returns a (non sorted) list, each element of which is the degree of one node of graph.
        '''
        return [self.graph.in_degree(node) for node in self.graph.nodes_iter()]
        #return [self.graph.in_degree(node) for node in self.graph.nodes_iter()]

    def get_degree_distribution(self):
        '''
        Returns a (non sorted) list, each element of which is the degree of one node of graph.
        '''
        return [self.graph.in_degree(node) + self.graph.node[node]['a'] * self.m for node in self.graph.nodes_iter() if self.graph.in_degree(node) + self.graph.node[node]['a'] * self.m > 1 ]
        #return [self.graph.in_degree(node) for node in self.graph.nodes_iter()]



class PowerlawFitting(object):
    """docstring for PowerlawFitting"""
    def __init__(self, degree_distribution, m, a, nb_runs):
        super(PowerlawFitting, self).__init__()
        self.degree_distribution = degree_distribution
        self.network_size = len(self.degree_distribution)
        self.m = m
        self.a = a
        self.nb_runs = nb_runs

        # declare internal fields initialized with stub values
        self.fit = None
        self.nu1 = 0.0
        self.D = 0.0
        self.xmin = 1.0 # we suspect the 'optimal' xmin to be greater than 1.0
        self.p_value = 0.0

        # the associated '_all' fields correspond to a xmin of m*a (or 1.0 in the traditional simple case of m = 1)
        self.fit_constrained = None
        self.nu1_constrained = 0.0
        self.D_constrained = 0.0
        self.p_value_constrained = 0.0


    def fit_to_powerLaw(self):
        '''
        Note: dd stands for self.degree_distribution
        list => {'nu1All':float, 'pvalueAll': float, 'nu1':float, 'pvalue':pvalue, 'xmin':xmin}
        Runs a goodness-of-fit test of the degree distribution dd to a power law.
        Null hypothesis: dd was generated by a power law + randomness

        Computes the following five values:
        1. nu1_all: an estimate for the exponent of the power function, fitted onto the whole distribution.
        2. pvalue_all: the probability that the observed data were generated by a power law with exponent nu1All. The null is rejected for pvalueAll < 0.1.
        3. nu1: an estimate for the exponent of the power function, fitted onto the distribution's upper tail x >= xmin.
        4. pvalue: the probability that the observed data were generated by a power law with exponent nu1. The null is rejected for pvalue < 0.1.
        5. xmin: the value of xmin that minizes the D statistic.

        Note : test based on Clauset et al. (2009)
        '''

        # we fit this degree distribution to a power law
        # the fitting routine uses a xmin value that minimizes
        # the distance of the given distribution to the fitted curve

        #### TRY TO FIT ON THE TRUNCATED PART ONLY ? + NOT SWITCHED 

        self.n_observations = len(self.degree_distribution)

        self.fit = powerlaw.Fit(self.degree_distribution, discrete = True, estimate_discrete=False) # creates the Fit object
        #self.nu1 = self.fit.power_law.alpha
        self.alpha = self.fit.power_law.alpha
        self.D = self.fit.power_law.D
        self.xmin = self.fit.power_law.xmin
        self.sigma = self.fit.power_law.sigma


        # we also compute the distance when taking the whole distribution
        # (that is, when forcing xmin = 0)

        kmin_constraint = 1.0 + self.m * self.a
        self.fit_constrained = powerlaw.Fit(self.degree_distribution, discrete = True, xmin = kmin_constraint, estimate_discrete=False) # creates a Fit object whil imposing the power law on the whole support
        #self.nu1_constrained = self.fit_all.power_law.alpha
        self.alpha_constrained = self.fit_constrained.power_law.alpha
        self.D_constrained = self.fit_constrained.power_law.D
        self.sigma_constrained = self.fit_constrained.power_law.sigma

        print 'fit_obj xmin = ', self.fit_constrained.power_law.xmin


        self.__get_observation_data__()

        # compute p_value for optimal xmin value
        synth_more_distant = 0
        for j in range (self.nb_runs): # corresponds to an estimate of p-value accurate to the second decimal point when nb_runs = 2500
            #synthData = self.__generate_synthetic_data__ (self.fit)
            synthData = self.__generate_synthetic_data__ (False)
            synthFit = powerlaw.Fit(synthData, discrete = True, estimate_discrete=False)
            synthD = synthFit.power_law.D
            if synthD > self.D:
                synth_more_distant += 1
        self.p_value = float(synth_more_distant) / nb_runs

        # compute p_value for whole distribution, that is force xmin = 1
        synth_more_distant = 0
        #average_distance = 0.0
        for j in range (self.nb_runs): # corresponds to an estimate of p-value accurate to the second decimal point when nb_runs = 2500
            #synthData = self.__generate_synthetic_data__(self.fit_constrained)
            synthData_constrained = self.__generate_synthetic_data__(True)
            synthFit_constrained = powerlaw.Fit(synthData_constrained, discrete = True, xmin = kmin_constraint, estimate_discrete=False)
            synthD = synthFit_constrained.power_law.D
            if synthD > self.D_constrained:
                synth_more_distant += 1
            #average_distance += synthD - self.D_constrained
        self.p_value_constrained = float(synth_more_distant) / nb_runs
        #average_distance /= nb_runs
        #print "the average constrained distance: ",average_distance

    def __get_observation_data__(self):
        # Note: the fit object knows about its xmin value

        # count how many nodes have a degree above or equal to xmin
        # this is stored in nTail
        ## in the new version this should be equal to the number of nodes in the "transformed" degree distribution ??
        #nTail = sum(map(lambda x: 1 if x >= fit_object.xmin else 0, self.degree_distribution))


        # additionally store the list of degrees (nodes) below xmin
        #lowerTail = [x for x in self.degree_distribution if x < fit_object.xmin]

        self.lowerTail = []
        for item in self.degree_distribution:
            if item < self.xmin:
                self.lowerTail.append(item)
        self.n_lowerTail = len(self.lowerTail)
        self.nTail = self.n_lowerTail - self.n_lowerTail
        # now compute probabilities to generate nodes in the upper vs. lower tail
        self.probUpperTail = float(self.nTail)/len(self.degree_distribution)


        #self.lowerTail = []
        #self.nTail = 0
        #self.n_lowerTail = 0
        #for x in self.degree_distribution:
        #    if x >= self.fit.xmin:
        #        self.nTail += 1
        #    else:
        #        self.lowerTail.append(x)
        #        self.n_lowerTail += 1

        print "size of the lower tail (unconstrained): ",self.n_lowerTail
        #if self.n_lowerTail == 0:
        #    print self.degree_distribution

        #self.lowerTail_constrained = []
        #self.nTail_constrained = 0
        #self.n_lowerTail_constrained = 0
        #for x in self.degree_distribution:
        #    if x >= self.fit_constrained.xmin:
        #        self.nTail_constrained += 1
        #    else:
        #        self.lowerTail.append(x)
        #        self.n_lowerTail += 1

        #print "size of the lower tail (contrained): ",self.n_lowerTail_constrained


    def __generate_synthetic_data__(self, constrained=False): # n, nTail):
    #def __generate_synthetic_data__(self, fit_object): # n, nTail):
        # Note: the fit object knows about its xmin value

        # count how many nodes have a degree above or equal to xmin
        # this is stored in nTail
        ## in the new version this should be equal to the number of nodes in the "transformed" degree distribution ??
        #nTail = sum(map(lambda x: 1 if x >= fit_object.xmin else 0, self.degree_distribution))


        # additionally store the list of degrees (nodes) below xmin
        #lowerTail = [x for x in self.degree_distribution if x < fit_object.xmin]

        #lowerTail = []
        #nTail = 0
        #n_lowerTail = 0
        #for x in self.degree_distribution:
        #    if x >= fit_object.xmin:
        #        nTail += 1
        #    else:
        #        lowerTail.append(x)
        #        n_lowerTail += 1

        #print "size of the lower tail: ",n_lowerTail
        
        # synthetic data is obtained using the following trick.
        # observation: there is probability p = nTail/self.network_size that a node is part of the end tail
        # toss a coin with probability p of success
        # if so use the fitted distribution to generate a node (its degree) part of the tail at random
        # if not draw a value at random from lowerTail

        #synthData = []
        #if constrained:
        #    for j in range (self.network_size):
        #        generated_value = self.fit_constrained.power_law.generate_random(1) if random.random() < float(self.nTail_constrained)/self.network_size or self.n_lowerTail_constrained==0 else random.sample(self.lowerTail_constrained, 1)
        #        synthData.append(float(generated_value[0]))
        #else:
        #    for j in range (self.network_size):
        #        generated_value = self.fit.power_law.generate_random(1) if random.random() < float(self.nTail)/self.network_size or self.n_lowerTail==0 else random.sample(self.lowerTail, 1)
        #        synthData.append(float(generated_value[0]))

        syntheticData = []
        if constrained == False:
            #print "of ",+self.n_observations," we have ", self.n_lowerTail, "in the lower tail with prob ", self.probUpperTail
            for j in range (self.n_observations):
                if rd.random() < self.probUpperTail or self.n_lowerTail == 0:

                    newDatapoint = self.xmin - 1
                    while newDatapoint < self.xmin:
                        newDatapoint = self.fit.power_law.generate_random(1)[0]
                        #print "newDatapoint:", newDatapoint 
                else:
                    newDatapoint = rd.choice(self.lowerTail)
                syntheticData.append(newDatapoint)


        else:

            syntheticData = self.fit_constrained.power_law.generate_random(self.n_observations)


        return syntheticData



'''
the next function is defined as external to the above classes
to make it easier to call them from the multiprocessing package
'''
def generate_and_fit_network(input_tuple):

    # input_tuple contains [m, networkSize, nu1, nu2, nb_runs] to feed the on-boarding model
    # plus the number of runs used to compute p_values
    m = input_tuple[0]
    networkSize =input_tuple[1]
    nu1 = input_tuple[2]
    nu2 = input_tuple[3]
    nb_runs = input_tuple[4]
    attractiveness = input_tuple[5]
    onBoard = input_tuple[6]

    print "initiating onboarding model"
    cm = OnBoardingModel(m, attractiveness, networkSize, nu1, nu2, onBoard)
    cm.generate()
    degree_distribution = cm.get_degree_distribution()
    #print "WOB =",cm.get_raw_degree_distribution()
    #print "generating tulip data"
    #cm.generate_tulip()
    #print "generated, getting degree distribution"
    #degree_distribution = cm.get_degree_distribution_tulip()
    print 'Network generated '

    pf = PowerlawFitting(degree_distribution, m, attractiveness, nb_runs)
    pf.fit_to_powerLaw()
    return ';'.join(map(lambda x: str(x), [pf.alpha_constrained, pf.sigma_constrained, pf.p_value_constrained, pf.alpha, pf.sigma, pf.p_value, pf.xmin, cm.get_raw_degree_distribution()]))


single_test = True
pack = False
if single_test:
    m = 1
    networkSize = 2000 # nb steps to iterate node addition, pref attach and on-boarding
    attractiveness = 1.0
    onBoard = True
    nu1 = 0.0
    nu2 = 0.0
    nb_runs = 2
    print '[m, networkSize, nu1, nu2, nb_runs, attractiveness, onBoard]', [m, networkSize, nu1, nu2, nb_runs, attractiveness, onBoard]
    for i in range(1):
        print generate_and_fit_network([m, networkSize, nu1, nu2, nb_runs, attractiveness, onBoard])


elif pack:
    # takes all files and compiles them into a single one
    path = '/Users/melancon/Documents/Recherche/Work in progress/Alberto/Fitting_statistics_2000/' # change this to your local path
    file_prefix = 'Fitting_statistics_2000_1_True_'
    file_suffix = '_1.0_2500.csv'
    out_file = 'All_fitting_statistics.csv'

    fp_out = open(path + out_file, 'w')

    fp_out.write('nu1;nu2;exp_all;pv_all;exp;pv;kmin;ob\n')
    for nu1 in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]: #, math.sqrt(0.33), math.sqrt(0.4), math.sqrt(0.5), math.sqrt(0.6), math.sqrt(0.67), math.sqrt(0.8)]:
        for nu2 in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
            fp_in = open(path + file_prefix + str(nu1) + '_' + str(nu2) + file_suffix, 'rU')
            line = fp_in.readline() # headers
            line = fp_in.readline()
            while line != '':
                items = [nu1, nu2] + line.strip().split(';') + [1]
                fp_out.write(';'.join(map(lambda x: str(x) , items)) + '\n')
                line = fp_in.readline()
            fp_in.close()

    file_name = 'Fitting_statistics_2000_1_False_1.0_2500.csv'
    fp_in = open(path + file_name, 'rU')
    line = fp_in.readline() # headers
    line = fp_in.readline()
    while line != '':
        items = ['', ''] + line.strip().split(';') + [0]
        fp_out.write(';'.join(map(lambda x: str(x) , items)) + '\n')
        line = fp_in.readline()
    fp_in.close()

    fp_out.close()


elif __name__ == '__main__':

    # Initialization
    m = 1
    networkSize = 2000 # nb steps to iterate node addition, pref attach and on-boarding
    attractiveness = 1.0
    onBoard = False
    nb_runs = 100
    #path = '/Users/albertocottica/Dropbox/PhD/Sunbelt paper/results/' # change this to your local path
    #path = '/net/cremi/gmelanco/Alberto/' # change this to your local path
    path = './results/'
    nb_workers = 4 #24 # 100

    if onBoard:

        for nu1 in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
            for nu2 in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
                print 'Dealing with nu1 = ', nu1, ' and nu2 = ', nu2

                filename = 'New_Fitting_statistics_' +  str(networkSize)  + '_' + str(m) + '_' + str(onBoard) + '_' + str(nu1) + '_' + str(nu2) + '_' + str(attractiveness)+'_' + str(nb_runs) + '.csv' # use a name with m and networkSize and trial number

                print 'Set all variables'

                # Real work starts here
                start = time.time()

                # number of workers is number of processes ran in parallel
                # this should ultimately be equal to the number of networks we wish to generate
                # builds an input_tuple fro each of the processes
                input_tuples = [[m, networkSize, nu1, nu2, nb_runs, attractiveness, onBoard] for graphNameIndex in range(nb_workers)]
                print 'Built tuples using m, networkSize, nu1, nu2, nb_runs, attractiveness, onBoard:'
                print [m, networkSize, nu1, nu2, nb_runs, attractiveness, onBoard]
                print input_tuples

                # processes are launched, the multiprocessing package takes care of dispatching things around
                p = Pool(nb_workers)

                all_stats = p.map(generate_and_fit_network, input_tuples)
                #stats = generate_and_fit_network(input_tuples[0])

                fp = open(path + filename, 'w')
                fp.write('alpha_constrained;sigma_constrained;p_value_constrained;alpha;sigma;p_value;x_min;original_degree_distribution\n')
                fp.write('\n'.join(map(lambda x: str(x), all_stats)))
                fp.close()

                print 'The whole thing took ', time.time()-start, ' seconds'
    else:

        print 'Dealing with onBoard = ', onBoard

        filename = 'Fitting_statistics_' +  str(networkSize)  + '_' + str(m) + '_' + str(onBoard) + '_' + str(attractiveness)+'_' + str(nb_runs) + '.csv'

        # Real work starts here
        start = time.time()

        # builds an input_tuple for each of the processes
        # nu1 nu2 take stub values because method generate requires these parameters although they are not used when onBoard == False
        nu1 = 0.0
        nu2 = 0.0
        input_tuples = [[m, networkSize, nu1, nu2, nb_runs, attractiveness, onBoard] for graphNameIndex in range(nb_workers)]
        print 'Built tuples using m, networkSize, nu1, nu2, nb_runs, attractiveness, onBoard:'
        print [m, networkSize, nu1, nu2, nb_runs, attractiveness, onBoard]

        # processes are launched, the multiprocessing package takes care of dispatching things around
        p = Pool(nb_workers)

        all_stats = p.map(generate_and_fit_network, input_tuples)
        #stats = generate_and_fit_network(input_tuples[0])

        fp = open(path + filename, 'w')
        fp.write('alpha_constrained;sigma_constrained;p_value_constrained;alpha;sigma;p_value;x_min;original_degree_distribution\n')
        fp.write('\n'.join(map(lambda x: str(x), all_stats)))
        fp.close()

        print 'The whole thing took ', time.time()-start, ' seconds'

