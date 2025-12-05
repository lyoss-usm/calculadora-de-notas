import numpy as np

def CC_certamen(x):
    certamenes = x[:3].copy()
    n_min = np.argmin(certamenes)
    certamenes[n_min] = x[2]

    NC = np.power(certamenes[2] * np.power((certamenes[0]+ certamenes[1])/2., 2.), 1/3)
    return NC

def CC_laboratorios(x):
    labs = x[3:8].copy()
    NPL1 = (np.sum(labs) - np.min(labs[np.array([0,1,3])]))/4

    min_lab = np.argmin(labs[[0,1,3]])
    labs[min_lab] = 0.
    sorted_labs = np.sort(labs)[::-1]


    w = np.array([0.35,0.35,0.15,0.15,0.])

    NPL2 = np.dot(sorted_labs, w)

    return max(NPL1, NPL2)

H = lambda x: 0 if x < 0. else 1.

NP = lambda x: (CC_certamen(x) * .75 + CC_laboratorios(x) * .25 * H(CC_laboratorios(x) - 55.)) * (x[8]/1000 + 1.)