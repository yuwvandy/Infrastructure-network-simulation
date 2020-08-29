module sf
    function list_adj(adjmatrix)
        #= Construct the adj2list map and list2adj map based on adjmatrix
        Input: adjmatrix - 2D array, the adjacent matrix of a network or a dependent network
        Output: adj2list - 2D array, adj2list[i, j]: the index number of link_{ij} in list
                list2adj - 2D array, list2adj[i, 1], list2adj[i, 2]: the row and column index of link i in the list
        =#
        rownum, columnnum = size(adjmatrix)[1], size(adjmatrix)[2]
        adj2list = Array{Int64}(undef, rownum, columnnum)
        list2adj = Array{Int64}(undef, Int64(sum(adjmatrix)), 2)

        temp = 0
        for i in 1:rownum
            for j in 1:columnnum
                if(adjmatrix[i, j] == 1)
                    temp += 1

                    adj2list[i, j] = temp
                    list2adj[temp, 1], list2adj[temp, 2] = i, j
                else
                    adj2list[i, j] = 0

                end
            end
        end

        return adj2list, list2adj
    end

    function array2dict(array, index1, index2)
        #= Construct the dictionary of the network information
        Input: array - 2D array of the network information
               index - the index of the network feature which requires number type of structure to save, not string
        Output: dictionary of the network information
        =#
        dict = Dict()
        for i in 1:(size(array)[1])
            if(i >= index1[1] && i <= index1[2])
                if( i >= index2[1] && i <= index2[2])
                    dict[array[i, 1]] = eval(Meta.parse(array[i, 2])).+1 #the difference of the start index between python and julia
                else
                    dict[array[i, 1]] = eval(Meta.parse(array[i, 2]))
                end
            else
                dict[array[i, 1]] = array[i, 2]
            end
        end
        return dict
    end
    #
    # function array2dict(array, index1, index2)
    #     #= Construct the dictionary of the network information
    #     Input: array - 2D array of the network information
    #            index - the index of the network feature which requires number type of structure to save, not string
    #     Output: dictionary of the network information
    #     =#
    #     dict = Dict()
    #     for i in 1:(size(array)[1])
    #         if(i >= index1[1] && i <= index1[2])
    #             if( i >= index2[1] && i <= index2[2])
    #                 dict[array[i, 1]] = eval(Meta.parse(array[i, 2])).+1 #the difference of the start index between python and julia
    #             else
    #                 dict[array[i, 1]] = eval(Meta.parse(array[i, 2]))
    #             end
    #         else
    #             dict[array[i, 1]] = array[i, 2]
    #         end
    #     end
    #     return dict
    # end

    function tranflowinout(Dict, Flow, Adj, adj2list)
        #= Set up the flow iterms going into and out of the transmission nodes
        Input: Dict - Dictionary of the network information
               Flow - The flow variable set up for the optimization problem
               Adj - 2D array, the adjacent matrix of the network
               adj2list - the map from the adjacent matrix to flow list
        Output: the array of flow going into and out of the certain nodes
        =#
        flowin = []
        flowout = []
        for i in 1:Dict["trannum"]
            trannum = Dict["transeries"][i]

            flowinnode = []
            flowoutnode = []
            for j in 1:Dict["nodenum"]
                if(Adj[j, trannum] == 1)
                    push!(flowinnode, Flow[adj2list[j, trannum]])
                end
                if(Adj[trannum, j] == 1)
                    push!(flowoutnode, Flow[adj2list[trannum, j]])
                end
            end
            if(length(flowinnode) == 0)
                push!(flowinnode, 0)
            end
            if(length(flowoutnode) == 0)
                push!(flowoutnode, 0)
            end

            push!(flowin, flowinnode)
            push!(flowout, flowoutnode)
        end
        return flowin, flowout
    end

    function demandflowinout(Dict, Flow, Adj, adj2list)
        #= Set up the flow iterms going into and out of the demand nodes
        Input: Dict - Dictionary of the network information
               Flow - The flow variable set up for the optimization problem
               Adj - 2D array, the adjacent matrix of the network
               adj2list - the map from the adjacent matrix to flow list
        Output: the array of flow going into and out of certain nodes
        =#
        flowin = []
        flowout = []
        for i in 1:Dict["demandnum"]
            demandnum = Dict["demandseries"][i]

            flowinnode = []
            flowoutnode = []
            for j in 1:Dict["nodenum"]
                if(Adj[j, demandnum] == 1)
                    push!(flowinnode, Flow[adj2list[j, demandnum]])
                end
                if(Adj[demandnum, j] == 1)
                    push!(flowoutnode, Flow[adj2list[demandnum, j]])
                end
            end

            if(length(flowinnode) == 0)
                push!(flowinnode, 0)
            end
            if(length(flowoutnode) == 0)
                push!(flowoutnode, 0)
            end

            push!(flowin, flowinnode)
            push!(flowout, flowoutnode)
        end
        return flowin, flowout
    end

    function demandinterflowout(interadj, dict1, dict2, interflow, adj2list)
        #= Set up the flow iterms going out from the demand nodes in network1 to supply nodes in network2, network1 -> network2
        Input: interadj - 2D array, the adjacent matrix of the interdependent network: demand nodes in network 2 -> supply nodes in network1
               interflow - The flow variable on interdependent links
               adj2list - the map from the adjacent matrix to flow list
               dict1, dict2 - the dictionary information of network1 and network2
        Output: the array of flow going out from demand nodes in network1 -> supply nodes in network2
        =#
        flowout = []
        for i in 1:dict1["demandnum"]
            flowoutnode = []
            for j in 1:dict2["supplynum"]
                if(interadj[i, j] == 1)
                    push!(flowoutnode, interflow[adj2list[i, j]])
                end
            end

            if(length(flowoutnode) == 0)
                push!(flowoutnode, 0)
            end

            push!(flowout, flowoutnode)
        end
        return flowout
    end

    function supplyinterflowin(interadj, dict1, dict2, interflow, adj2list)
        #= Set up the flow iterms going into the supply nodes in network2 from demand nodes in network1
        Input: interadj - 2D array, the adjacent matrix of the interdependent network: demand nodes in network 2 -> supply nodes in network1
               interflow - The flow variable on interdependent links
               adj2list - the map from the adjacent matrix to flow list
               dict1, dict2 - the dictionary information of network1 and network2
        Output: the array of flow going out from demand nodes in network1 -> supply nodes in network2
        =#
        flowin = []
        for i in 1:dict2["supplynum"]
            flowinnode = []
            for j in 1:dict1["demandnum"]
                if(interadj[j, i] == 1)
                    push!(flowinnode, interflow[adj2list[j, i]])
                end
            end

            if(length(flowinnode) == 0)
                push!(flowinnode, 0)
            end

            push!(flowin, flowinnode)
        end
        return flowin
    end

    function pdemandwlinkflowout(demand2linkadj, flow, dict, link2nodeid, distnode2node)
        #= Set up the power required for transport water in water networks
        Input: demand2linkadj: the adj matrix from demand nodes in network1 to the links in networks
               flow: the flow variable generated for optimization in network2
               link2nodeid: the function mapping the link in network2 to the nodes at the ends of the links in network2
               distnode2node: the distance between nodes in network2
        Output: flow going out of the demand node in network1, height and distance to calculate the energy loss
        =#
        flowout = []
        H1 = []
        H2 = []
        L = []
        for i in 1:size(demand2linkadj)[1]
            flowoutnode = []
            H1node, H2node = [], []
            Lnode = []
            for j in 1:size(demand2linkadj)[2]
                if(demand2linkadj[i, j] == 1)
                    push!(flowoutnode, flow[j])
                    push!(H1node, dict["elevation"][Int64(link2nodeid[j, 1])])
                    push!(H2node, dict["elevation"][Int64(link2nodeid[j, 2])])
                    push!(Lnode, distnode2node[Int64(link2nodeid[j, 1]), Int64(link2nodeid[j, 2])])
                end
            end
            push!(flowout, flowoutnode)
            push!(H1, H1node)
            push!(H2, H2node)
            push!(L, Lnode)
        end
        return flowout, H1, H2, L
    end

    function pdemandwpinterlinkflowout(demand2linkadj, flow, dict1, dict2, link2nodeid, distnode2node)
        #= Set up the power required for transport water flow between water and power networks
        Input: demand2linkadj: the adj matrix from demand nodes in network3 to the interdependent links between network1 and 2
               flow: the flow variable generated for optimization in internetwork
               link2nodeid: the function mapping the link in internetwork to the nodes at the ends of the links in network1 and 2
               distnode2node: the distance between nodes in network1 and nodes in network2
        Output: flow going out of the demand node in network3, height and distance to calculate the energy loss
        =#
        flowout = []
        H1 = []
        H2 = []
        L = []
        for i in 1:size(demand2linkadj)[1]
            flowoutnode = []
            H1node, H2node = [], []
            Lnode = []
            for j in 1:size(demand2linkadj)[2]
                if(demand2linkadj[i, j] == 1)
                    push!(flowoutnode, flow[j])
                    push!(H1node, dict1["elevation"][dict1["demandseries"][Int64(link2nodeid[j, 1])]])
                    push!(H2node, dict2["elevation"][dict2["supplyseries"][Int64(link2nodeid[j, 2])]])
                    push!(Lnode, distnode2node[Int64(link2nodeid[j, 1]), Int64(link2nodeid[j, 2])])
                end
            end
            push!(flowout, flowoutnode)
            push!(H1, H1node)
            push!(H2, H2node)
            push!(L, Lnode)
        end
        return flowout, H1, H2, L
    end

    function pdemandglinkflowout(demand2linkadj, flow, Pr, link2nodeid)
        #= Set up the power required for transport Gas in Gas networks
        Input: demand2linkadj: the adj matrix from demand nodes in network1 to the links in networks
               flow: the flow variable generated for optimization in network2
               Pr: the pressure variable generated for optimization in network2
        Output: flow and pressure of links depending on demand nodes in network1
        =#
        flowout = []
        Pr1 = []
        Pr2 = []
        for i in 1:size(demand2linkadj)[1]
            flowoutnode = []
            Pr1node, Pr2node = [], []
            for j in 1:size(demand2linkadj)[2]
                if(demand2linkadj[i, j] == 1)
                    push!(flowoutnode, flow[j])
                    push!(Pr1node, Pr[Int64(link2nodeid[j, 1])])
                    push!(Pr2node, Pr[Int64(link2nodeid[j, 2])])
                end
            end
            push!(flowout, flowoutnode)
            push!(Pr1, Pr1node)
            push!(Pr2, Pr2node)
        end
        return flowout, Pr1, Pr2
    end

    function pdemandgpinterlinkflowout(demand2linkadj, flow, pr1, pr2, dict1, dict2, link2nodeid)
        #= Set up the power required for transport gas flow between gas and power networks
        Input: demand2linkadj: the adj matrix from demand nodes in network3 to the interdependent links between network1 and 2
               flow: the flow variable generated for optimization in internetwork
               link2nodeid: the function mapping the link in internetwork to the nodes at the ends of the links in network1 and 2
               pr1: the pressure variable in gas networks
               pr2: the pressure variable in power networks (power supply nodes)
        Output: flow going out of the demand node in network3, height and distance to calculate the energy loss
        =#
        flowout = []
        Pr1 = []
        Pr2 = []
        for i in 1:size(demand2linkadj)[1]
            flowoutnode = []
            Pr1node, Pr2node = [], []
            for j in 1:size(demand2linkadj)[2]
                if(demand2linkadj[i, j] == 1)
                    push!(flowoutnode, flow[j])
                    push!(Pr1node, pr1[dict1["demandseries"][Int64(link2nodeid[j, 1])]])
                    push!(Pr2node, pr2[dict2["supplyseries"][Int64(link2nodeid[j, 2])]])
                end
            end
            push!(flowout, flowoutnode)
            push!(Pr1, Pr1node)
            push!(Pr2, Pr2node)
        end
        return flowout, Pr1, Pr2
    end

    function zeropad(array)
        #=add zero element to the none entry of the array
        Input: array - 1D array
        Output: the updated array where the none entry originally becomes 0 entry
        =#
        for i in 1:length(array)
            if(length(array[i]) == 0)
                array[i] = [0]
            end
        end
        return array
    end

    # function importcsv(array)
    #     #=save the optimization result to CSV
    #     =#
    #     x =
end
