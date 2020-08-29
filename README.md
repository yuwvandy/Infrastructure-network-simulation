# Interdependent Infrastructure Network Simulation Tool
A comprehensive framework to simulate interdependent infrastructure networks as well as their physical flow, which can be used as test cases for vulnerability assessment and restoration optimization of interdependent infrastructure networks.

![simulated system](https://user-images.githubusercontent.com/53798810/91645022-2c78b400-ea07-11ea-8c45-fe8ed01903ec.png)

## 1. Motivation
Interdependent infrastructure networks provide essential services to modern societies and their disruptions could lead to the catastrophic outcomes, which necessitates the evaluation of their system-level performance. Typically, the system-level performance is assessed by taking real networks as testbeds, simulating failure scenarios and measuring their performance decay along the time. 
## 2. Input data
(1) The area where the infrastructure systems are to be set up: geographical boundary (lat, lon), the population distribution (in tract sense), the real infrastructure system to be simulated (degree distribution, the number of different type of facilities)
## Output data
(1) The interdependent system to be simulated: the topology and the flow
## 3. Contents
**** 
### Network topology simulation and analysis are performed in Python
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
**** 
### Flow simulation is performed through nonliear optimization, which is set up and solved in Julia with Juniper package
* mainprogramming.jl: the main function to set up the solver, decision variables, linear and nonlinear constraints
* python2juliadata.jl: the function to import network data from python to julia
* Sharefunction.jl: the general functions which are shared by all julia scripts in the project
* dataopt.jl: the value of the parameters in the optimization
**** 
### Folder of data
* Edges.xlsx, Nodes.xlsx: the pipeline (grid) and facility information of the gas, power and water infrastructure networks in Shelby County
* Tract.xlsx: The population distribution in Shelby County
**** 
### Folder of PDF
* Interdependent_network_optimization for network flow.pdf: the mathematical formalization of the network flow optimization problem

## 4. To run
First load all modules except the Shelby_County_network.py, the topologyanalysis.py, main.py, mainprogramming.jl
**** 
### For simulating network topology and performing statistical analysis:
* Execuate the Shelby_County_network.py, then run the topologyanalysis.py
**** 
#### For simulating network topology and optimizaion to solve the network flow:
* Execuate the main.py and mainprogramming.jl
