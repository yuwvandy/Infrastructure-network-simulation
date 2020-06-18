#=The script is to load the data defined by Python
The data is used for defining the programming variables in julia
=#

using CSV
using Formatting
#Read the csv file in the current folder and import data
#adjacent and distance matrix
path = string(pwd(), "/p2jdata/adjdist")
filelist = readdir(path)

for i in range(1, length(filelist))
    print(filelist[i])
    varname = chop(filelist[i], tail = 4)
    temppath = string(path, "/$(filelist[i])")
    CSV.read(temppath, datarow = 1)
    eval(Meta.parse("$(varname) = Matrix(CSV.read(temppath, datarow = 1))"))
end


#network information
path = string(pwd(), "/p2jdata/networkinfo")
filelist = readdir(path)

for i in range(1, length(filelist))
    print(filelist[i])
    varname = chop(filelist[i], tail = 4)
    temppath = string(path, "/$(filelist[i])")
    eval(Meta.parse("$(varname) = Matrix(CSV.read(temppath, datarow = 1))"))
end
