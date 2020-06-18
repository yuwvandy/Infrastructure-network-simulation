using Juniper
using JuMP
using Ipopt
using GLPK

include("python2juliadata.jl")
#Define the network nodes
gasnum = size(Gasadj)[1]
powernum = size(Poweradj)[1]
waternum = size(Wateradj)[1]

#Define transformation mapping: list2adj and adj2list
Gadj2list, Glist2adj = sf.list_adj(Gasadj)
Padj2list, Plist2adj = sf.list_adj(Poweradj)
Wadj2list, Wlist2adj = sf.list_adj(Wateradj)

GPadj2list, GPlist2adj = sf.list_adj(gdemand2psupplyadj)
PGadj2list, PGlist2adj = sf.list_adj(pdemand2glinkadj)
PWadj2list, PWlist2adj = sf.list_adj(pdemand2wlinkadj)
WPadj2list, WPadj2list = sf.list_adj(wdemand2psupplyadj)

#Model set up
mp = Model(Juniper.Optimizer)

#------------------------------------------------Define the programming variables
#network
@variable(mp, Gflow[1:size(Glist2adj)[1]] >= 0)
@variable(mp, Pload[1:powernum])
@variable(mp, Wflow[1:size(Wlist2adj)[1]] >= 0)
@variable(mp, Gpr[1:gasnum] >= 0)
#between network
@variable(mp, GPflow[1:size(GPlist2adj)[1]] >= 0)
@variable(mp, PGload[1:size(PGlist2adj)[1]] >= 0)
@variable(mp, PWload[1:size(PWlist2adj)[1]] >= 0)
@variable(mp, WPflow[1:size(WPlist2adj)[1]] >= 0)

#------------------------------------------------Define the constraints
#flow conservation for water transmission nodes

#flow conservation for gas transmission nodes

#flow conservation for water demand nodes

#flow conservation for gas demand nodes
