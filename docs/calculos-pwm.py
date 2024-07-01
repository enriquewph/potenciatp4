#!/usr/bin python

# utilizamos el RC3525a para generar una señal PWM de 10KHz, 20KHz y 80KHz seleccionables


freq = [10000, 20000, 80000] # Frecuencias de 10KHz, 20KHz y 80KHz

#capas disponibles 1.2nF, 3.9nF, 4.7nF, 8.2nF
caps = [1.2e-9, 3.9e-9, 4.7e-9, 8.2e-9]

#valores de resistencias comerciales 5%
r_commercial = [1, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
r_commercial_multiplier = [0.1, 1, 10, 100, 1000, 10000, 100000, 1000000]
#generar lista de valores comerciales de resistencias con su string asociado dependiendo del multiplicador
r_commercial_values = []
for r in r_commercial:
    for m in r_commercial_multiplier:
        r_commercial_values.append(r*m)
#ordenar ascendente
r_commercial_values.sort()

Rd = 100 # Resistencia de descarga de 100 Ohm segun recomendacion de la pag. 14

#ecuacion fo: pagina 5 del datasheet

#fo = 1/(cap * (0.7*Rt+3*Rd))

# calculamos Rt para cada frecuencia
res = [[0 for x in range(len(freq))] for y in range(len(caps))]

for c in caps:
    for f in freq:
        Rt = (1/(f*c) - 3*Rd)/0.7
        res[caps.index(c)][freq.index(f)] = Rt
        
for c in caps:
    # determinar la resistencia comercial maxima que cumple con el minimo Rt, el resto asignarlo en Rt_var
    min_res = min(res[caps.index(c)]) - 1000
    max_res = max(res[caps.index(c)])
    Rt_fijo = 0
    for r in r_commercial_values:
        Rt_fijo = r
        if r >= min_res:
            break
    Rt_var = []
    for r in res[caps.index(c)]:
        Rt_var.append(r - Rt_fijo)
        
    Rt_var_min = min(Rt_var)
    Rt_var_max = max(Rt_var)
    
    #print("Para C = %.1f nF" % (c*1e9))
    #print("Rt fijo: %.1f Ohm" % Rt_fijo)
    #print("Rt variable: %.1f - %.1f Ohm" % (Rt_var_min, Rt_var_max))
            
#Para C = 8.2 nF
#Rt fijo: 820.0 Ohm
#Rt variable: 929.1 - 16173.0 Ohm
                
for c in caps:
    for f in freq:
        print("f: %d kHz, c: %.1f nF -> Rt:%.1f Ohm" % (f/1e3, c*1e9, res[caps.index(c)][freq.index(f)]))