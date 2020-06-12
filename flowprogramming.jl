using Juniper
using JuMP
using Ipopt
using Cbc

optimizer = Juniper.Optimizer
nl_solver = optimizer_with_attributes(Ipopt.Optimizer, "print_level"=>0)

using LinearAlgebra # for the dot product
m = Model(optimizer_with_attributes(optimizer, "nl_solver"=>nl_solver))

v = [10,20,12,23,42]
w = [12,45,12,22,21]
@variable(m, x[1:5], Bin)

@objective(m, Max, dot(v,x))

@NLconstraint(m, sum(w[i]*x[i]^2 for i=1:5) <= 45)

optimize!(m)

# retrieve the objective value, corresponding x values and the status
println(JuMP.value.(x))
println(JuMP.objective_value(m))
println(JuMP.termination_status(m))

optimizer = Juniper.Optimizer
nl_solver= optimizer_with_attributes(Ipopt.Optimizer, "print_level" => 0)
mip_solver = optimizer_with_attributes(Cbc.Optimizer, "logLevel" => 0)
m = Model(optimizer_with_attributes(optimizer, "nl_solver"=>nl_solver, "mip_solver"=>mip_solver))
