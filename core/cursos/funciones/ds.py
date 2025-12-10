import numpy as np

def NP(x):
    w = np.array([0.5, 0.3, 0.1, 0.1])
    notas = np.array([
        np.mean(x[:2]),   # Promedio de los certámenes
        x[2],             # Nota del proyecto
        np.mean(x[3:8]),  # Promedio de las tareas
        np.mean(x[8:]),   # Promedio de los quizzes
    ])

    return np.dot(w, notas)