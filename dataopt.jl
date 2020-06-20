module dt
#For equation (8): gas combustion -> electricity
au, bu, cu = 1, 1, 1 #temporarily assumed
H = 50 #MJ/kg
kapa = 1 #convertion ratio for water cooling effect using power

#For equation (9)-(10): electricity -> pressure increase of compressor
K = 1.38 #isentropic exponent
Z = 1.0# gas compressibility factor: 0.8-1.2
R = 8314.51 #Universal Gas Constant which is a scalar parameter
elta = 0.85 #Adiabatic efficiency
T = 140 #Celsius

#For equation (11)-(13): electricity -> pressure increase to transport water flow
wdensity = 1000 #kg/m^3
g = 9.8 #gravity acceleration
beta = 130 #based on the materials of the pipelines, the values of different materials are listed in URL:https://www.engineeringtoolbox.com/hazen-williams-coefficients-d_798.html

#For equation (19): gas pressure and gas flow
delta1, delta2, delta3, delta4, delta5 = 18.0625, 2.6667, 1.0, 1.0, 0.5 #Take the method of Weymouth
e = 0.92 #efficiency factor of the gas pipelines
xi = 0.5537# (pure methane) the specific gravity of gas, relative to air: the ratio of the density of the gas at standard pressure and temperature to the density of air
phi = 1.0 #gas compressibility: different from the gas compressibility factor Z above
Ts = 520 #Temperature at standard condition: Rankine
Prs = 14.73 #Pressure at standard condition: psia
end
