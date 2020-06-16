#=The script is to load the data defined by Python
The data is used for defining the programming variables in julia
=#

using CSV
using Formatting
##Change the current working directory to p2jdata
print("Current directory:", pwd())

#Read the csv file in the current folder and import data
filelist = readdir()
for i in range(1, length(filelist))
    varname = chop(filelist[i], tail = 4)
    eval(Meta.parse("$(varname) = Matrix(CSV.read(\"./$(filelist[i])\"))"))
end
