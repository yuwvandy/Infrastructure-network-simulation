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
        for i in range(1, rownum)
            for j in range(1, columnnum)
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
                push!(flowinnode, 0)
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
                push!(flowinnode, 0)
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
end
