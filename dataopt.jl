module dt
#For equation (8): gas combustion -> electricity
au, bu, cu = 1, 1, 1 #temporarily assumed
H = 35396 #kJ/m^3
kapa = 1.8/1000 #convertion ratio for water cooling effect using power: how much water (m^3) do we need generate electricity per kWh

#For equation (9)-(10): electricity -> pressure increase of compressor
K = 1.38 #isentropic exponent
Z = 1.0# gas compressibility factor: 0.8-1.2
R = 8314.51 #Universal Gas Constant which is a scalar parameter
elta = 0.85 #Adiabatic efficiency
T = 70 #Celsius

gasdensity = 0.7 #kg/m^3
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

#For objective (equation (29))
cw, cg, cp = 1, 1, 1 #the cost of transport single unit of flow per unit distance

# powerperunit = 0.000488 #KW*h/s https://www.eia.gov/tools/faqs/faq.php?id=97&t=3
powervar_spring = [0.000369, 0.000354, 0.000344, 0.000339, 0.000339, 0.000351, 0.000371, 0.000418, 0.00046, 0.000467, 0.000457, 0.000448, 0.000442, 0.000431, 0.000424, 0.000417, 0.000412, 0.000409, 0.00041, 0.000412, 0.000417, 0.000435, 0.000441, 0.000422]
powervar_summer = [0.000484, 0.000448, 0.000423, 0.000405, 0.000392, 0.000391, 0.000402, 0.000424, 0.00045, 0.000476, 0.000501, 0.000528, 0.000553, 0.000582, 0.000605, 0.000616, 0.000623, 0.000623, 0.000622, 0.000616, 0.000605, 0.000586, 0.000578, 0.000555]
powervar_autumn = [0.000371, 0.000351, 0.000336, 0.000326, 0.000326, 0.000328, 0.000342, 0.000369, 0.000405, 0.00041, 0.000414, 0.000417, 0.000423, 0.000423, 0.000429, 0.000429, 0.000428, 0.000426, 0.00043, 0.000434, 0.00045, 0.000451, 0.000439, 0.000416]
powervar_winter = [0.000396, 0.000374, 0.00036, 0.000349, 0.000346, 0.000345, 0.000352, 0.000381, 0.000413, 0.00042, 0.000418, 0.000419, 0.000424, 0.000424, 0.000421, 0.000421, 0.00042, 0.000422, 0.000432, 0.000454, 0.000452, 0.000445, 0.000434, 0.000414]

powervar = [powervar_spring, powervar_summer, powervar_autumn, powervar_winter]

gasperunit = 0.000648*0.02831 #m^3/s
waterperunit = 3.942e-6 #m^3/s

waterdiameter = 0.6 #m
gasdiameter = 0.7 #m
end
