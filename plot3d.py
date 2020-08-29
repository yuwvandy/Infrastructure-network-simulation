# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 20:26:50 2020

@author: 10624
"""

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

def Plot3d1(Networks, InterNetworks):
    fig = plt.figure(figsize = (20, 15))
    ax = fig.add_subplot(111, projection = '3d')
    ZZ = [400, 200, 0]
    
    temp = 0
    for network in Networks:
        x, y = np.arange(0, 70, 1), np.arange(0, 70, 1)
        x, y = np.meshgrid(x, y)
        z = np.array([[ZZ[temp]]*len(x)]*len(y), dtype = float)
        
        temp += 1
        
        X = network.x/1000
        Y = network.y/1000
        if(network.name == 'Gas'):
            Z = np.array([ZZ[0]]*network.nodenum, dtype = float)
        if(network.name == 'Power'):
            Z = np.array([ZZ[1]]*network.nodenum, dtype = float)
        if(network.name == 'Water'):
            Z = np.array([ZZ[2]]*network.nodenum, dtype = float)
        
        network.Z = Z
        network.X = X
        network.Y = Y
        
        #Network nodes plots
        ax.scatter3D(X[network.supplyseries], Y[network.supplyseries], Z[network.supplyseries], \
                     depthshade = False, zdir = 'z', marker = '+', color = network.color, \
                         label = network.supplyname, s = 80)
        ax.scatter3D(X[network.transeries], Y[network.transeries], Z[network.transeries], \
                     depthshade = False, zdir = 'z', marker = '*', color = network.color, \
                         label = network.tranname, s = 60)
        ax.scatter3D(X[network.demandseries], Y[network.demandseries], Z[network.demandseries], \
                     depthshade = False, zdir = 'z', marker = 'o', color = network.color, \
                         label = network.demandname, s = 40)
            
        ax.plot_surface(x, y, z, linewidth=0, antialiased=False, alpha=0.05, color = network.color)
        
        #Link plots
        ##link in the network
        for i in range(len(network.Adjmatrix)):
            for j in range(len(network.Adjmatrix)):
                if(network.Adjmatrix[i, j] == 1):
                    ax.plot([X[i], X[j]], [Y[i], Y[j]], [Z[i], Z[j]], 'black', lw = 1)
    
    for network in InterNetworks:
        for i in range(network.nodenum1):
            if(network.__class__.__name__ == 'phynode2node'):
                for j in range(network.nodenum2):
                    if(network.adjmatrix[i, j] == 1):
                            ax.plot([network.network1.X[network.network1.demandseries[i]], network.network2.X[network.network2.supplyseries[j]]], \
                                    [network.network1.Y[network.network1.demandseries[i]], network.network2.Y[network.network2.supplyseries[j]]], \
                                    [network.network1.Z[0], network.network2.Z[0]], 'purple', linestyle = "--", lw = 1)
            
            # if(network.__class__.__name__ == 'phynode2link'):
            #     for j in range(network.linknum2):
            #             ax.plot([network.network1.X[network.network1.demandseries[i]], network.network2.edgelist[j]["middlex"]/1000], \
            #                     [network.network1.Y[network.network1.demandseries[i]], network.network2.edgelist[j]["middley"]/1000], \
            #                     [network.network1.Z[0], network.network2.Z[0]], 'purple')
                        
                    # if(network.__class__.__name__ == 'phynode2interlink'):
                    #     ax.plot([network.network3.X[network.network3.demandseries[i]], network.network2.edgelist[j]["middlex"]/1000, \
                    #             [network.network3.Y[network.network3.demandseries[i]], network.network2.edgelist[j]["middley"]/1000, \
                    #             [network.network3.Z[0], network.network2.Z[0], 'purple')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0.85), ncol=3, shadow=False, frameon = 0)
    
def Plot3d2(Networks, InterNetworks):
    fig = plt.figure(figsize = (20, 15))
    ax = fig.add_subplot(111, projection = '3d')
    ZZ = [400, 200, 0]
    
    temp = 0
    for network in Networks:
        x, y = np.arange(0, 70, 1), np.arange(0, 70, 1)
        x, y = np.meshgrid(x, y)
        z = np.array([[ZZ[temp]]*len(x)]*len(y), dtype = float)
        
        temp += 1
        
        X = network.x/1000
        Y = network.y/1000
        if(network.name == 'Gas'):
            Z = np.array([ZZ[0]]*network.nodenum, dtype = float)
        if(network.name == 'Power'):
            Z = np.array([ZZ[1]]*network.nodenum, dtype = float)
        if(network.name == 'Water'):
            Z = np.array([ZZ[2]]*network.nodenum, dtype = float)
        
        network.Z = Z
        network.X = X
        network.Y = Y
        
        #Network nodes plots
        ax.scatter3D(X[network.supplyseries], Y[network.supplyseries], Z[network.supplyseries], \
                     depthshade = False, zdir = 'z', marker = '+', color = network.color, \
                         label = network.supplyname, s = 80)
        ax.scatter3D(X[network.transeries], Y[network.transeries], Z[network.transeries], \
                     depthshade = False, zdir = 'z', marker = '*', color = network.color, \
                         label = network.tranname, s = 60)
        ax.scatter3D(X[network.demandseries], Y[network.demandseries], Z[network.demandseries], \
                     depthshade = False, zdir = 'z', marker = 'o', color = network.color, \
                         label = network.demandname, s = 40)
            
        ax.plot_surface(x, y, z, linewidth=0, antialiased=False, alpha=0.05, color = network.color)
        
        #Link plots
        ##link in the network
        for i in range(len(network.Adjmatrix)):
            for j in range(len(network.Adjmatrix)):
                if(network.Adjmatrix[i, j] == 1):
                    ax.plot([X[i], X[j]], [Y[i], Y[j]], [Z[i], Z[j]], 'black', lw = 1)
    
    for network in InterNetworks:
        for i in range(network.nodenum1):
            # if(network.__class__.__name__ == 'phynode2node'):
            #     for j in range(network.nodenum2):
            #         if(network.adjmatrix[i, j] == 1):
            #                 ax.plot([network.network1.X[network.network1.demandseries[i]], network.network2.X[network.network2.supplyseries[j]]], \
            #                         [network.network1.Y[network.network1.demandseries[i]], network.network2.Y[network.network2.supplyseries[j]]], \
            #                         [network.network1.Z[0], network.network2.Z[0]], 'purple', linestyle = "--", lw = 1)
            
            if(network.__class__.__name__ == 'phynode2link'):
                for j in range(network.linknum2):
                    if(network.adjmatrix[i, j] == 1):
                        ax.plot([network.network1.X[network.network1.demandseries[i]], network.network2.edgelist[j]["middlex"]/1000], \
                                [network.network1.Y[network.network1.demandseries[i]], network.network2.edgelist[j]["middley"]/1000], \
                                [network.network1.Z[0], network.network2.Z[0]], 'purple', lw = 1, linestyle = '--')
                        
                    # if(network.__class__.__name__ == 'phynode2interlink'):
                    #     ax.plot([network.network3.X[network.network3.demandseries[i]], network.network2.edgelist[j]["middlex"]/1000, \
                    #             [network.network3.Y[network.network3.demandseries[i]], network.network2.edgelist[j]["middley"]/1000, \
                    #             [network.network3.Z[0], network.network2.Z[0], 'purple')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0.85), ncol=3, shadow=False, frameon = 0)
    
def Plot3d3(Networks, InterNetworks):
    fig = plt.figure(figsize = (20, 15))
    ax = fig.add_subplot(111, projection = '3d')
    ZZ = [400, 200, 0]
    
    temp = 0
    for network in Networks:
        x, y = np.arange(0, 70, 1), np.arange(0, 70, 1)
        x, y = np.meshgrid(x, y)
        z = np.array([[ZZ[temp]]*len(x)]*len(y), dtype = float)
        
        temp += 1
        
        X = network.x/1000
        Y = network.y/1000
        if(network.name == 'Gas'):
            Z = np.array([ZZ[0]]*network.nodenum, dtype = float)
        if(network.name == 'Power'):
            Z = np.array([ZZ[1]]*network.nodenum, dtype = float)
        if(network.name == 'Water'):
            Z = np.array([ZZ[2]]*network.nodenum, dtype = float)
        
        network.Z = Z
        network.X = X
        network.Y = Y
        
        #Network nodes plots
        ax.scatter3D(X[network.supplyseries], Y[network.supplyseries], Z[network.supplyseries], \
                     depthshade = False, zdir = 'z', marker = '+', color = network.color, \
                         label = network.supplyname, s = 80)
        ax.scatter3D(X[network.transeries], Y[network.transeries], Z[network.transeries], \
                     depthshade = False, zdir = 'z', marker = '*', color = network.color, \
                         label = network.tranname, s = 60)
        ax.scatter3D(X[network.demandseries], Y[network.demandseries], Z[network.demandseries], \
                     depthshade = False, zdir = 'z', marker = 'o', color = network.color, \
                         label = network.demandname, s = 40)
            
        ax.plot_surface(x, y, z, linewidth=0, antialiased=False, alpha=0.05, color = network.color)
        
        #Link plots
        ##link in the network
        # for i in range(len(network.Adjmatrix)):
        #     for j in range(len(network.Adjmatrix)):
        #         if(network.Adjmatrix[i, j] == 1):
        #             ax.plot([X[i], X[j]], [Y[i], Y[j]], [Z[i], Z[j]], 'black', lw = 1)
    
    for network in InterNetworks:
        if(network.__class__.__name__ == 'phynode2node'):
            for i in range(network.nodenum1):
                for j in range(network.nodenum2):
                    if(network.adjmatrix[i, j] == 1):
                            ax.plot([network.network1.X[network.network1.demandseries[i]], network.network2.X[network.network2.supplyseries[j]]], \
                                    [network.network1.Y[network.network1.demandseries[i]], network.network2.Y[network.network2.supplyseries[j]]], \
                                    [network.network1.Z[0], network.network2.Z[0]], 'purple', linestyle = "--", lw = 1)
            
            # if(network.__class__.__name__ == 'phynode2link'):
            #     for j in range(network.linknum2):
            #         if(network.adjmatrix[i, j] == 1):
            #             ax.plot([network.network1.X[network.network1.demandseries[i]], network.network2.edgelist[j]["middlex"]/1000], \
            #                     [network.network1.Y[network.network1.demandseries[i]], network.network2.edgelist[j]["middley"]/1000], \
            #                     [network.network1.Z[0], network.network2.Z[0]], 'purple', lw = 1, linestyle = '--')
        if(network.__class__.__name__ == 'phynode2interlink'):
            for i in range(network.nodenum3):
                for j in range(network.linknum):
                    if(network.adjmatrix[i, j] == 1):
                        ax.plot([network.network3.X[network.network3.demandseries[i]], network.internet1net2.edgelist[j]["middlex"]/1000],\
                                [network.network3.Y[network.network3.demandseries[i]], network.internet1net2.edgelist[j]["middley"]/1000],\
                                [network.network3.Z[0], 0.5*(network.internet1net2.network1.Z[0]+network.internet1net2.network2.Z[0])], 'green', linestyle = '--')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0.85), ncol=3, shadow=False, frameon = 0)





Plot3d1([Gas, Power, Water], [gdemand2psupply, wdemand2psupply, pdemand2glink, pdemand2wlink])
Plot3d1([Power, Water], [wdemand2psupply, pdemand2wlink])
Plot3d2([Gas, Power, Water], [gdemand2psupply, wdemand2psupply, pdemand2glink, pdemand2wlink])
Plot3d2([Power, Water], [wdemand2psupply, pdemand2wlink])
Plot3d3([Power, Water], [wdemand2psupply, pdemand2wlink, pdemand2wpinterlink])
plt.savefig("./visualsystem1.pdf", dpi = 1500, bbox_inches='tight', pad_inches=0)
    
        
        
        
        
        
        
        