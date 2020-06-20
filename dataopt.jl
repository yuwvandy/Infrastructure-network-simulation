module dt
#For equation (8): gas combustion -> electricity
au, bu, cu = 1, 1, 1 #temporarily assumed
H = 50 #MJ/kg
kapa = 1 #convertion ratio for water cooling effect using power

#For equation (9)-(10): electricity -> pressure increase of compressor
K = 1.38 #isentropic exponent
Z = 1.0# gas compressibility factor: 0.8-1.2
Rs = 8314.51 #Universal Gas Constant which is a scalar parameter
elta = 0.85 #Adiabatic efficiency
T = 140 #Celsius

#For equation (11)-(13): electricity -> pressure increase to transport water flow
wdensity = 1000 #kg/m^3
g = 9.8 #gravity acceleration
beta = 130 #based on the materials of the pipelines, the values of different materials are listed in URL:https://www.engineeringtoolbox.com/hazen-williams-coefficients-d_798.html

end
