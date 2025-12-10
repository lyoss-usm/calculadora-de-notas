import numpy as np

def NP(x):
    prom_quizzes = (np.sum(x[1:6]) - np.min(x[1:6])) / (len(x[1:6]) - 1)
    prom_casos = (np.sum(x[6:11]) - np.min(x[6:11])) / (len(x[6:11]) - 1)
    prom_anteproyecto = np.dot(x[11:15], np.array([0.05,0.05,0.05,0.2]))
    certamen = x[0]
    informe_final = x[-1]

    if certamen >= 55. and informe_final >= 55.:
        return certamen*0.3 + prom_quizzes*0.15 + prom_casos*0.2 + prom_anteproyecto
    else:
        return min(certamen, informe_final)
