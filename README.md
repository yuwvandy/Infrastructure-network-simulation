# Simulation tool of interdependent gas-power-water systems
## Motivation
Developing a tool which can simulate infrastructure networks and their interdependencies, initialize the network flow inter and intro networks.
## Input data
(1) The area where the infrastructure systems are to be set up: geographical boundary (lat, lon), the population distribution (in tract sense), the real infrastructure system to be simulated (degree distribution, the number of different type of facilities)
## Output data
(1) The interdependent system to be simulated
## Contents
* Basemapset.py: Set up the base backgroud where the infrastructure system is to be set; import the population data here
* Annealing simulation.py: Heuristic search to solve the optimal facility location problem
* Network.py: Network object specificed to define the infrastructure networks; Several important network operations are included: random bipartite graph algorithm, find all paths between certain pair of nodes (i, j), calculate different network topologies
* Sharefunction.py: include the basic function that can be used in general way, shared by all other scripts in the folder
* topologyanalysis.py: initialize networks several times and perform statistical anlaysis of the network topology feature, compare it with networks simulated using other methods (ouyang methods and features of real networks)
* Networkouyang.py: set up networks using ouyang methods
* data.py: specified the data we use for each parameter
* Tract.py: import the population data in tract scale
* Randomlinknetwork.py: Randomly distribute the nodes in 2D plane and connect them only considering the geographical distance
* Shelby_County_network.py: set up the realistic networks in Shelby County
