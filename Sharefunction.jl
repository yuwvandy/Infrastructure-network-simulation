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
end
