import numpy as np

def NP(x):
    prom_quizzes = np.mean(x[:3])
    prom_tareas = np.mean(x[3:])

    return 0.4 * prom_quizzes + 0.6 * prom_tareas