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
###------------------flow conservation
#for transmission nodes in water networks
Wtflowin, Wtflowout = sf.tranflowinout(Waterdict, Wflow, Wateradj, Wadj2list)
@constraint(mp, Wtconserve[i = 1:Waterdict["trannum"]], sum(Wtflowin[i]) == sum(Wtflowout[i]))

#for transmission nodes in gas networks
Gtflowin, Gtflowout = sf.tranflowinout(Gasdict, Gflow, Gasadj, Gadj2list)
@constraint(mp, Gtconserve[i = 1:Gasdict["trannum"]], sum(Gtflowin[i]) == sum(Gtflowout[i]))

#for demand nodes in water networks
#flow in and out within demand nodes in the water networks
Wdflowin, Wdflowout1 = sf.demandflowinout(Waterdict, Wflow, Wateradj, Wadj2list)
#flow: water demand -> power supply
Wdflowout2 = sf.demandinterflowout(wdemand2psupplyadj, Waterdict, Powerdict, WPflow, WPadj2list)
#flow: water demand -> residents
Wdflowout3 = Waterdict["population_assignment"]
@constraint(mp, Wdconserve[i = 1:Waterdict["demandnum"]], sum(Wdflowin[i]) == sum(Wdflowout2[i]) + sum(Wdflowout3[i]))

#for demand nodes in gas networks
#flow in and out within demand nodes in the gas networks
Gdflowin, Gdflowout1 = sf.demandflowinout(Gasdict, Gflow, Gasadj, Gadj2list)
#flow: gas demand -> power supply
Gdflowout2 = sf.demandinterflowout(gdemand2psupplyadj, Gasdict, Powerdict, GPflow, GPadj2list)
#flow: Gas demand -> residents
Gdflowout3 = Gasdict["population_assignment"]
@constraint(mp, Gdconserve[i = 1:Gasdict["demandnum"]], sum(Gdflowin[i]) == sum(Gdflowout2[i]) + sum(Gdflowout3[i]))

###------------------dependency of power supply nodes on gas demand nodes
GdflowinPs = sf.supplyinterflowin(gdemand2psupplyadj, Gasdict, Powerdict, GPflow, GPadj2list)
@constraint(mp, GdPsinter[i = 1:Powerdict["supplynum"]], sum(GdflowinPs[i]) == 1/data.H*(data.au + data.bu*Pload[i] + data.cu*Pload[i]^2))

###------------------dependency of power supply nodes on water demand nodes
WdflowinPs = sf.supplyinterflowin(wdemand2psupplyadj, Waterdict, Powerdict, WPflow, WPadj2list)
@constraint(mp, WdPsinter[i = 1:Powerdict["supplynum"]], sum(WdflowinPs[i]) == data.kapa*Pload[i])

###------------------dependency of gas links on power demand nodes

###------------------dependency of water links on power demand nodes

###------------------relationship between pressure and gas flow of gas links
###
