using Juniper
using JuMP
using Ipopt
using GLPK

include("python2juliadata.jl")

#Define transformation mapping: list2adj and adj2list
Gadj2list, Glist2adj = list_adj(Gasadj)
Padj2list, Plist2adj = list_adj(Poweradj)
Wadj2list, Wlist2adj = list_adj(Wateradj)

GPadj2list, GPlist2adj = list_adj(gdemand2psupplyadj)
PGadj2list, PGlist2adj = list_adj(pdemand2glinkadj)
PWadj2list, WPlist2adj = list_adj(pdemand2wlinkadj)
WPadj2list, WPadj2list = list_adj(wdemand2psupplyadj)
