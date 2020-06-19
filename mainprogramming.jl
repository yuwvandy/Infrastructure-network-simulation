using Juniper
using JuMP
using Ipopt
using GLPK

include("python2juliadata.jl")
#Define the network nodes
gnum, gdemandnum, gtransnum, gsupplynum = Gasdict["nodenum"], Gasdict["demandnum"], Gasdict["trannum"], Gasdict["supplynum"]
pnum, pdemandnum, ptransnum, psupplynum = Powerdict["nodenum"], Powerdict["demandnum"], Powerdict["trannum"], Powerdict["supplynum"]
wnum, wdemandnum, wtransnum, wsupplynum = Waterdict["nodenum"], Waterdict["demandnum"], Waterdict["trannum"], Waterdict["supplynum"]

#Define transformation mapping: list2adj and adj2list
Gadj2list, Glist2adj = sf.list_adj(Gasadj)
Padj2list, Plist2adj = sf.list_adj(Poweradj)
Wadj2list, Wlist2adj = sf.list_adj(Wateradj)

GPadj2list, GPlist2adj = sf.list_adj(gdemand2psupplyadj)
PGadj2list, PGlist2adj = sf.list_adj(pdemand2glinkadj)
PWadj2list, PWlist2adj = sf.list_adj(pdemand2wlinkadj)
WPadj2list, WPlist2adj = sf.list_adj(wdemand2psupplyadj)

#Model set up
mp = Model(Juniper.Optimizer)

#------------------------------------------------Define the programming variables
#network
@variable(mp, Gflow[1:size(Glist2adj)[1]] >= 0)
@variable(mp, Pload[1:pnum])
@variable(mp, Wflow[1:size(Wlist2adj)[1]] >= 0)
@variable(mp, Gpr[1:gnum] >= 0)
#between network
@variable(mp, GPflow[1:size(GPlist2adj)[1]] >= 0)
@variable(mp, PGload[1:size(PGlist2adj)[1]] >= 0)
@variable(mp, PWload[1:size(PWlist2adj)[1]] >= 0)
@variable(mp, WPflow[1:size(WPlist2adj)[1]] >= 0)


#------------------------------------------------Constraints
###flow conservation
#for transmission nodes in water networks
Wtflowin, Wtflowout = sf.tranflowinout(Waterdict, Wflow, Wateradj, Wadj2list)
@constraint(mp, Wtconserve[i = 1:length(Wtflowin)], sum(Wtflowin[i]) == sum(Wtflowout[i]))

#for transmission nodes in gas networks
Gtflowin, Gtflowout = sf.tranflowinout(Gasdict, Gflow, Gasadj, Gadj2list)
@constraint(mp, Gtconserve[i = 1:length(Gtflowin)], sum(Gtflowin[i]) == sum(Gtflowout[i]))

#for demand nodes in water networks
#flow in and out within demand nodes in the water networks
Wdflowin, Wdflowout1 = sf.demandflowinout(Waterdict, Wflow, Wateradj, Wadj2list)
#flow: water demand -> power supply
Wdflowout2 = sf.demandinterflowout(wdemand2psupplyadj, Waterdict, Powerdict, WPflow, WPadj2list)
#flow: water demand -> residents
Wdflowout3 = Waterdict["population_assignment"]
@constraint(mp, Wdconserve[i = 1:length(Wdflowin)], sum(Wdflowin[i]) == sum(Wdflowout2[i]) + sum(Wdflowout3[i]))

#for demand nodes in gas networks
#flow in and out within demand nodes in the gas networks
Gdflowin, Gdflowout1 = sf.demandflowinout(Gasdict, Gflow, Gasadj, Gadj2list)
#flow: gas demand -> power supply
Gdflowout2 = sf.demandinterflowout(gdemand2psupplyadj, Gasdict, Gasdict, GPflow, GPadj2list)
#flow: Gas demand -> residents
Gdflowout3 = Gasdict["population_assignment"]
@constraint(mp, Gdconserve[i = 1:length(Gdflowin)], sum(Gdflowin[i]) == sum(Gdflowout2[i]) + sum(Gdflowout3[i]))


#flow conservation for water demand nodes

#flow conservation for gas demand nodes
