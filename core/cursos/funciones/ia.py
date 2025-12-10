import numpy as np

def NP(x):
    prom_certamenes = np.mean(x[:2])
    nota_proyecto = x[2]

    if prom_certamenes >= 50.:
        nota_presentacion = prom_certamenes * 0.6 + nota_proyecto * 0.4
    else:
        nota_presentacion = prom_certamenes
    return nota_presentacion