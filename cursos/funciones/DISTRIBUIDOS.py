import numpy as np


def S(x):
    prom_certamenes = np.mean(x[:2])
    quizzes = x[5:].copy()
    quizzes = np.sort(quizzes)[1:]  
    prom_quizzes = np.mean(quizzes)

    return 2 / 3 * prom_certamenes + 1 / 3 * prom_quizzes


def alpha(S_val):
    if S_val <= 40:
        return 0.
    elif S_val < 55:
        return (S_val - 40.) / 15
    else:
        return 1.

def NP(x):
    S_val = S(x)
    alpha_val = alpha(S_val)

    prom_tareas = np.mean(x[2:5])

    return (1 - 0.3*alpha_val) * S_val + 0.3 * alpha_val * prom_tareas
