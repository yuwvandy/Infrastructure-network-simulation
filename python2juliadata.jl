#=The script is to load the data defined by Python
The data is used for defining the programming variables in julia
=#

using CSV
using Formatting
#Read the csv file in the current folder and import data
#adjacent and distance matrix
path = string(pwd(), "/p2jdata/adjdist")
filelist = readdir(path)
filepath = Array{String}(undef, length(filelist))

for i in 1:length(filelist)
    varname = chop(filelist[i], tail = 4)
    filepath[i] = string(path, "/$(filelist[i])")
    eval(Meta.parse("$(varname) = Matrix(CSV.read(filepath[$(i)], datarow = 1))"))
end

#network information
path = string(pwd(), "/p2jdata/networkinfo")
filelist = readdir(path)
filepath = Array{String}(undef, length(filelist))

for i in 1:length(filelist)
    varname = chop(filelist[i], tail = 4)
    filepath[i] = string(path, "/$(filelist[i])")
    eval(Meta.parse("$(varname) = Matrix(CSV.read(filepath[$(i)], datarow = 1))"))
end


#network information transformation: array 2 dict
Gasdict = sf.array2dict(Gasdata, [5, 13], [9, 11])
Powerdict = sf.array2dict(Powerdata, [5, 13], [9, 11])
Waterdict = sf.array2dict(Waterdata, [5, 13], [9, 11])
