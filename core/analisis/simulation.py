from core.cursos import Curso
import numpy as np
from core.utils import AppConfig
import matplotlib.pyplot as plt


def get_sample(curso: Curso):
    """
    Genera n muestras aleatorias para las notas que falten por completar en un curso.
    Utiliza la configuracion del curso para determinar el numero de muestras y las notas ya completadas.
    Las notas ya completadas se mantienen fijas, mientras que las notas faltantes se generan aleatoriamente.
    :param curso: Curso al que se le generará la muestra.
    :return: Un array de numpy con las muestras generadas.
    """
    cfg = AppConfig()
    n = cfg.get("n_samples", 1000)

    notas = curso.get_notas()
    bools = curso.get_bools()
    k = notas.shape[0]

    sample = np.random.random((n, k)) * 100.

    sample = sample * ~bools + notas

    return sample


def montecarlo(curso: Curso):
    """
    Realiza una simulación de Monte Carlo para la nota de presentación de un curso.
    :param curso:
    :return: notas, mask_obj, mask_aprobado
    """
    sample = get_sample(curso)
    notas = np.apply_along_axis(curso.func, axis=1, arr=sample)

    cfg = config.Config()
    nota_aprobada = cfg.get("nota_aprobar", 55)

    obj = curso.objetivo
    mask_obj = notas >= obj

    mask_aprobado = (notas >= nota_aprobada) & ~mask_obj

    return notas, mask_obj, mask_aprobado


def plot_histogram(notas: np.ndarray, mask_obj: np.ndarray, mask_aprobado: np.ndarray, curso: Curso):
    """
    Genera el histograma de la distribución de notas simuladas para un curso.

    Args:
      notas: Array de numpy con las notas simuladas (np.ndarray).
      mask_obj: Máscara booleana para las notas que alcanzan el objetivo (np.ndarray).
      mask_aprobado: Máscara booleana para las notas aprobadas (np.ndarray).
      curso: Instancia del curso para el cual se generará el histograma (Curso).
    """
    nota_max = np.max(notas)

    plt.figure(figsize=(10, 6))
    plt.hist(notas, bins=50)

    plt.title(f"Distribución simulada para {curso.nombre}")
    plt.xlabel("NP")
    plt.xlim(0, max(nota_max, 100))
    plt.ylabel("Frecuencia")

    # Análisis de resultados
    print(f"Resultados de la simulación para el curso {curso.nombre}:")

    n = len(notas)
    n_aprobado = np.sum(mask_aprobado)
    n_objetivo = np.sum(mask_obj)
    n_reprobado = n - n_aprobado - n_objetivo

    perc_reprobado = n_reprobado / n
    perc_aprobado = (n_aprobado+n_objetivo) / n
    perc_objetivo = n_objetivo / n

    print(f"Se reprobó en el             {perc_reprobado * 100:.2f}% de los casos.")
    print(f"Se aprobó en el              {perc_aprobado * 100:.2f}% de los casos.")
    print(f"Se alcanzó el objetivo en el {perc_objetivo * 100:.2f}% de los casos.")
    print()

    notas = curso.get_notas()
    bools = curso.get_bools()
    nota_actual = curso.func(notas)
    nota_max = curso.func(notas + 100. * ~bools)

    print(f"Nota actual:            {nota_actual:.2f}")
    print(f"Nota máxima alcanzable: {nota_max:.2f}")
    plt.show()
