import numpy as np

def NP(x):
    trabajos = x[2:-2]
    trabajos = np.sort(trabajos)[2:]
    prom_trabajos = np.mean(trabajos)
    prom_proyectos = np.mean(x[-2:]) # 

    return 0.3*(x[0] + x[1]) + prom_trabajos * 0.2 + prom_proyectos * 0.2