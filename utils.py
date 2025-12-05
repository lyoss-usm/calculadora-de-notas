import json
import numpy as np

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def get_evals_arrays(evals):
    """
    Extracts the first element from each evaluation in the list.
    """
    names = np.array([eval[0] for eval in evals], dtype=str)
    notas = np.array([eval[1] for eval in evals], dtype=float)
    bools = np.array([eval[2] for eval in evals], dtype=bool)
    indep = np.array([eval[3] for eval in evals], dtype=bool)

    return names, notas, bools, indep