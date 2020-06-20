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

PWinterlinkadj2list, PWinterlinkadjlist2adj = sf.list_adj(pdemand2wpinterlinkadj)
PGinterlinkadj2list, PGinterlinklist2adj = sf.list_adj(pdemand2gpinterlinkadj)

#Model set up
mp = Model(Juniper.Optimizer)

#------------------------------------------------Define the programming variables
#network
@variable(mp, Gflow[1:size(Glist2adj)[1]] >= 0)
@variable(mp, Pload[1:pnum])
@variable(mp, Wflow[1:size(Wlist2adj)[1]] >= 0)
@variable(mp, Gpr[1:gnum] >= 0)
@variable(mp, Ppr[1:psupplynum] >= 0)
#between network
@variable(mp, GPflow[1:size(GPlist2adj)[1]] >= 0)
@variable(mp, PGload[1:size(PGlist2adj)[1]] >= 0)
@variable(mp, PWload[1:size(PWlist2adj)[1]] >= 0)
@variable(mp, WPflow[1:size(WPlist2adj)[1]] >= 0)


#------------------------------------------------Constraints
###------------------flow conservation
#for transmission nodes in water networks
Wtflowin, Wtflowout = sf.tranflowinout(Waterdict, Wflow, Wateradj, Wadj2list)
@constraint(mp, Wtconserve[i = 1:wtransnum], sum(Wtflowin[i]) == sum(Wtflowout[i]))

#for transmission nodes in gas networks
Gtflowin, Gtflowout = sf.tranflowinout(Gasdict, Gflow, Gasadj, Gadj2list)
@constraint(mp, Gtconserve[i = 1:gtransnum], sum(Gtflowin[i]) == sum(Gtflowout[i]))

#for demand nodes in water networks
#flow in and out within demand nodes in the water networks
Wdflowin, Wdflowout1 = sf.demandflowinout(Waterdict, Wflow, Wateradj, Wadj2list)
#flow: water demand -> power supply
Wdflowout2 = sf.demandinterflowout(wdemand2psupplyadj, Waterdict, Powerdict, WPflow, WPadj2list)
#flow: water demand -> residents
Wdflowout3 = Waterdict["population_assignment"]
@constraint(mp, Wdconserve[i = 1:wdemandnum], sum(Wdflowin[i]) == sum(Wdflowout2[i]) + sum(Wdflowout3[i]))

#for demand nodes in gas networks
#flow in and out within demand nodes in the gas networks
Gdflowin, Gdflowout1 = sf.demandflowinout(Gasdict, Gflow, Gasadj, Gadj2list)
#flow: gas demand -> power supply
Gdflowout2 = sf.demandinterflowout(gdemand2psupplyadj, Gasdict, Powerdict, GPflow, GPadj2list)
#flow: Gas demand -> residents
Gdflowout3 = Gasdict["population_assignment"]
@constraint(mp, Gdconserve[i = 1:gdemandnum], sum(Gdflowin[i]) == sum(Gdflowout2[i]) + sum(Gdflowout3[i]))

#for demand and supply nodes in power networks
#power load of demand nodes equal to the power load of supply nodes
@constraint(mp, Pdsconserve, sum(Pload[Powerdict["supplyseries"][i]] for i in 1:length(psupplynum)) == sum(Pload[Powerdict["demandseries"][i]] for i in 1:length(pdemandnum)))

###------------------dependency of power supply nodes on gas demand nodes
GdflowinPs = sf.supplyinterflowin(gdemand2psupplyadj, Gasdict, Powerdict, GPflow, GPadj2list)
@NLconstraint(mp, GdPsinter[i = 1:psupplynum], sum(GdflowinPs[i][j] for j in 1:length(GdflowinPs[i])) == 1/dt.H*(dt.au + dt.bu*Pload[i] + dt.cu*Pload[i]^2))

###------------------dependency of power supply nodes on water demand nodes
WdflowinPs = sf.supplyinterflowin(wdemand2psupplyadj, Waterdict, Powerdict, WPflow, WPadj2list)
@constraint(mp, WdPsinter[i = 1:psupplynum], sum(WdflowinPs[i]) == dt.kapa*Pload[i])

###------------------dependency of water links on power demand nodes
#water links in water networks
PdWlflowout1, H1_1, H2_1, L_1 = sf.pdemandwlinkflowout(pdemand2wlinkadj, Wflow, Waterdict, pdemand2wlinklink2nodeid, Waterdistnode2node)
#water links from water demand nodes to power supply nodes
PdWlflowout2, H1_2, H2_2, L_2 = sf.pdemandwpinterlinkflowout(pdemand2wpinterlinkadj, WPflow, Waterdict, Powerdict, pdemand2wpinterlinklink2nodeid, wdemand2psupplydistnode2node)

PdWlflowout1, H1_1, H2_1, L_1 = sf.zeropad(PdWlflowout1), sf.zeropad(H1_1), sf.zeropad(H2_1), sf.zeropad(L_1)
PdWlflowout2, H1_2, H2_2, L_2 = sf.zeropad(PdWlflowout2), sf.zeropad(H1_2), sf.zeropad(H2_2), sf.zeropad(L_2)

###-----------------dependency of gas links on power demand nodes
#gas links in gas networks
PdGlflowout1, Pr1_1, Pr2_1 = sf.pdemandglinkflowout(pdemand2glinkadj, Gflow, Gpr, pdemand2glinklink2nodeid)
PdGlflowout1, Pr1_1, Pr2_1 = sf.zeropad(PdGlflowout1), sf.zeropad(Pr1_1), sf.zeropad(Pr2_1)
#gas links from gas demand nodes to power supply nodes
PdGlflowout2, Pr1_2, Pr2_2 = sf.pdemandgpinterlinkflowout(pdemand2gpinterlinkadj, GPflow, Gpr, Ppr, Gasdict, Powerdict, pdemand2gpinterlinklink2nodeid)
PdGlflowout2, Pr1_2, Pr2_2 = sf.zeropad(PdGlflowout2), sf.zeropad(Pr1_2), sf.zeropad(Pr2_2)


@NLconstraint(mp, Pdwglink[i = 1:pdemandnum], sum(dt.wdensity*dt.g*PdWlflowout1[i][j]*(H2_1[i][j] - H1_1[i][j]) for j in 1:length(H2_1[i])) +
            sum(10.654*(PdWlflowout1[i][j]/dt.beta)^1.852*(L_1[i][j]/Waterdict["edgediameter"]) for j in 1:length(H2_1[i])) +
            sum(dt.wdensity*dt.g*PdWlflowout2[i][j]*(H2_2[i][j] - H1_2[i][j]) for j in 1:length(H2_2[i])) +
            sum(10.654*(PdWlflowout2[i][j]/dt.beta)^1.852*(L_2[i][j]/Waterdict["edgediameter"]) for j in 1:length(H2_2[i])) +
            sum((dt.Z*dt.R*dt.T/((dt.K - 1)*dt.K)*((Pr2_1[i][j]/Pr1_1[i][j])^((dt.K-1)/dt.K) - 1))*PdGlflowout1[i][j]/(33000*dt.elta) for j in 1:length(Pr2_1[i])) +
            sum((dt.Z*dt.R*dt.T/((dt.K - 1)*dt.K)*((Pr2_2[i][j]/Pr1_2[i][j])^((dt.K-1)/dt.K) - 1))*PdGlflowout2[i][j]/(33000*dt.elta) for j in 1:length(Pr2_2[i])) +
            Powerdict["population_assignment"][i] == Pload[Powerdict["demandseries"][i]])

#pressure and flow constraint in gas networks
@NLconstraint(mp, Glinkprflow[i = 1:length(Gflow)], Gflow[i] == dt.delta1*dt.e*(Gasdict["edgediameter"])^dt.delta2*(dt.Ts/dt.Prs)^dt.delta3*((Gpr[Glist2adj[i, 1]]^2 - Gpr[Glist2adj[i, 2]]^2)/(dt.xi^dt.delta4*Gasdistnode2node[Glist2adj[i, 1], Glist2adj[i, 2]]*dt.T*dt.phi))^dt.delta5)
#pressure and flow constraint in interdependent gas-power networks
@NLconstraint(mp, G2Plinkprflow[i = 1:length(GPflow)], GPflow[i] == dt.delta1*dt.e*(Gasdict["edgediameter"])^dt.delta2*(dt.Ts/dt.Prs)^dt.delta3*((Gpr[Gasdict["demandseries"][GPlist2adj[i, 1]]]^2 - Ppr[Powerdict["supplyseries"][GPlist2adj[i, 2]]]^2)/(dt.xi^dt.delta4*gdemand2psupplydistnode2node[GPlist2adj[i, 1], GPlist2adj[i, 2]]*dt.T*dt.phi))^dt.delta5)

@objective(mp, Min, sum(Wflow[i]*Waterdistnode2node[Wlist2adj[i, 1], Wlist2adj[i, 2]] for i in 1:length(Wflow))*dt.cw +
                    sum(Gflow[i]*Gasdistnode2node[Glist2adj[i, 1], Glist2adj[i, 2]] for i in 1:length(Gflow))*dt.cg +
                    sum(Pload[i] for i in Powerdict["supplyseries"])*dt.cp +
                    sum(WPflow[i]*wdemand2psupplydistnode2node[WPlist2adj[i, 1], WPlist2adj[i, 2]] for i in 1:length(WPflow))*dt.cw +
                    sum(GPflow[i]*gdemand2psupplydistnode2node[GPlist2adj[i, 1], GPlist2adj[i, 2]] for i in 1:length(GPflow))*dt.cg)
