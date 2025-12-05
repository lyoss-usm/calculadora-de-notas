import os
import webbrowser
import numpy as np
from cursos.curso import Curso
from config import Config
import matplotlib.pyplot as plt
from numpy.ma.core import masked
import plotly.graph_objects as go
import plotly.colors as pc
from scipy.optimize import root_scalar

def find_nota(f, x0, x1 , nota_ind, notas_dep, notas_ind, n_conv):
    """
    Se utiliza el método de la secante para encontrar la nota que hace que la función f sea igual a la nota deseada.

    :param f: Función a la que se le quiere encontrar la raíz.
    :param nota_ind: Nota independiente.
    :param notas_dep: Array donde se guardarán las notas dependientes (raíz).
    :param notas_ind: Array donde se guardarán las notas independientes (nota).
    :param n_conv: Índice del array donde se guardará la próxima convergencia.
    :return: 1 si el método convergió, 0 si no.
    """
    '''if f(-20) * f(120) > 0:
        return 0'''
    
    if x0 == x1:
        x1 += 1e-8

    root = root_scalar(f, method='secant', x0=x0, x1=x1)

    if root['converged']:
        r = root['root']

        if np.abs(f(r)) > 1e-3:
            return 0

        if r < -20. or r > 120.:
            return 0

        notas_dep[n_conv] = r
        notas_ind[n_conv] = nota_ind
        return 1

    return 0

def obtener_notas(curso: Curso, nota):
    """
    Obtiene la curva de nivel "nota" para la nota de presentación del curso.

    :param curso: Instancia de la clase Curso.
    :param nota: Nota de presentación deseada.
    :return: Dos arrays: uno con las notas independientes y otro con las notas dependientes.
    """
    notas = curso.get_notas()
    cfg = Config()
    n = int(cfg.get("n_discretizacion", 200)*1.2)
    eje_x = np.linspace(-10,110,n)
    f = curso.func

    rendida = curso.get_bools()
    indep = curso.get_indep()
    notas_ind = np.zeros(n+2)
    notas_dep = np.zeros(n+2)
    n_conv = 0

    mask_indep = ~rendida & indep
    mask_dep = ~rendida & ~indep

    for i in np.arange(n):
        notas[mask_indep] = eje_x[i]
        fr = lambda x: f(notas + mask_dep*x) - nota
        if n_conv == 0:
            x0 = 0.
            x1 = 100.
        elif n_conv == 1:
            x0 = notas_dep[0]
            x1 = notas_dep[0] + 1e-8
        else:
            dy = notas_dep[n_conv-1] - notas_dep[n_conv-2]
            h = 1e-7
            x0 = notas_dep[n_conv-1] - dy * h
            x1 = notas_dep[n_conv-1] + dy * h
        conv = find_nota(fr, x0, x1, eje_x[i], notas_dep, notas_ind, n_conv)
        n_conv += conv

    order = np.argsort(notas_ind[:n_conv])

    return notas_ind[:n_conv][order], notas_dep[:n_conv][order]

def plot_NP(curso: Curso):
    """
    Gráfico de la nota de presentación en función de una evaluación restante.
    :param curso: Instancia de la clase Curso.
    :return: None
    """
    nota_restante = ~curso.get_bools()
    evaluacion_restante = curso.get_evaluaciones()[nota_restante][0]
    notas = curso.get_notas()
    cfg = Config()
    n = cfg.get("n_discretizacion", 200)

    x = np.linspace(0, 100, n)

    # REVISAR, CREO Q SE PUEDE VECTORIZAR BN
    fr = lambda nota: curso.func(notas + nota_restante * nota)
    NP = np.zeros(n)

    # este es el for a vectorizar
    for i in np.arange(n):
        NP[i] = fr(x[i])

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x,
        y=NP,
        mode='lines',
        name='NP',
        line=dict(color='royalblue')
    ))

    fig.update_layout(
        title=f"Nota de presentación de {curso.nombre} en función de {evaluacion_restante}",
        dragmode=False,

        xaxis=dict(
            title=evaluacion_restante,
            range=[0, 100],
            dtick=5,
            minor=dict(dtick=5),
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray',
            minor_griddash='dot',
            minor_gridcolor='rgba(0,0,0,0.2)',
            zeroline=True,
        ),
        yaxis=dict(
            title="NP",
            range=[0, max(100, np.max(NP))],
            dtick=5,
            minor=dict(dtick=5),
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray',
            minor_griddash='dot',
            minor_gridcolor='rgba(0,0,0,0.2)',
            zeroline=True,
        ),
        height=900,
        width=900
    )

    nombre_archivo = os.path.join("graficos", f"{curso.nombre}.html")
    fig.write_html(nombre_archivo)

    firefox = webbrowser.get(using='firefox')
    firefox.open_new_tab(f"file://{os.path.abspath(nombre_archivo)}")

def plot_notas(curso: Curso):
    """
    Dependiendo de la cantidad de evaluaciones que faltan por rendir, se genera un gráfico diferente:
    - Si no quedan evaluaciones, se muestra la nota obtenida.
    - Si queda una evaluación, se muestra la nota de presentación en función de esa evaluación.
    - Si quedan más de una evaluación, se muestra la curva de nivel de nota de presentación.

    :param curso: Instancia de la clase Curso.
    :return: None
    """
    notas = curso.get_notas()
    rendida = curso.get_bools()
    cfg = Config()

    n_rendida = np.sum(~rendida)

    if n_rendida == 0:
        NP = curso.func(notas)
        print(f"Nota obtenida: {NP:.2f}")
        if NP < cfg.get("nota_aprobar", 55):
            print("No aprobaste el curso.")
        elif NP < curso.objetivo:
            print("Aprobaste el curso, pero no alcanzaste el objetivo.")
        else:
            print("Aprobaste el curso y alcanzaste el objetivo! Felicidades!")
        return

    if n_rendida == 1:
        plot_NP(curso)
        return

    evaluaciones = curso.get_evaluaciones()
    indep = curso.get_indep()
    mask_indep = ~rendida & indep
    mask_dep = ~rendida & ~indep

    if np.sum(mask_indep) == 0 or np.sum(mask_dep) == 0:
        print("No hay evaluaciones independientes o dependientes disponibles.")
        return

    names_ind = ', '.join(evaluaciones[mask_indep])
    names_dep = ', '.join(evaluaciones[mask_dep])

    fig = go.Figure()

    range_obj = cfg.get("cortes", [55, 70, 80, 90, 100])

    for obj in range_obj:
        x, y = obtener_notas(curso, obj)

        if len(x) == 0:
            continue

        perc = obj / 100

        if cfg.get("inverse_cmap", False):
            perc = 1 - perc

        color = pc.sample_colorscale('Portland', [perc])[0]

        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='lines',
            name=f"NP {obj}",
            line=dict(
                width=2,
                color=color,
            ),
        ))

    fig.update_layout(
        title=f"Curvas de nivel de nota de presentación de {curso.nombre}",
        dragmode=False,

        xaxis=dict(
            title=names_ind,
            range=[0, 100],
            dtick=5,
            minor=dict(dtick=5),
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray',
            minor_griddash='dot',
            minor_gridcolor='rgba(0,0,0,0.2)',
            zeroline=True,
        ),
        yaxis=dict(
            title=names_dep,
            range=[0, 100],
            dtick=5,
            minor=dict(dtick=5),
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray',
            minor_griddash='dot',
            minor_gridcolor='rgba(0,0,0,0.2)',
            zeroline=True,
        ),
        height=900,
        width=900
    )

    nombre_archivo = os.path.join("graficos", f"{curso.nombre}.html")
    fig.write_html(nombre_archivo)

    firefox = webbrowser.get(using='firefox')
    firefox.open_new_tab(f"file://{os.path.abspath(nombre_archivo)}")