import numpy as np
from ..cursos.evaluator import eval_node

def find_nota_necesaria(model, empty_evals, target_final, x0=None):
    '''
    Encuentra la nota necesaria en las evaluaciones vacías para alcanzar la nota final objetivo.

    - Utiliza el método de Newton-Raphson para encontrar la raíz de la función que representa la diferencia entre la nota final calculada y la nota final objetivo.
    - Se aproxima la derivada mediante diferencias finitas usando forward-difference con h=1e-6.

    :param model: Diccionario que contiene el AST y el contexto de evaluación
    :param empty_evals: Lista de índices de evaluaciones vacías
    :param target_final: Nota final objetivo
    '''
    AST = model['AST']
    ctx = model['context']
    evals = np.array(ctx['values'], dtype=np.float64)

    def f(nota):
        evals[empty_evals] = nota
        ctx['values'] = evals.tolist()
        final_grade = eval_node(AST, ctx)
        return final_grade - target_final

    if x0 is None:
        x0 = target_final

    max_iter = 100
    tol = 1e-7
    for i in range(max_iter):
        f_x0 = f(x0)
        if not np.isfinite(f_x0):
            return None
        if abs(f_x0) < tol:
            return x0

        h = 1e-6
        f_x0_h = f(x0 + h)
        if not np.isfinite(f_x0_h):
            return None

        derivative = (f_x0_h - f_x0) / h

        # evitar derivada 0 o demasiado pequeña o no finita, porque sino Newton se vuelve loco, o salta mucho de un valor a otro, o div por cero.
        if (not np.isfinite(derivative)) or abs(derivative) < 1e-12:
            derivative = 1e-6

        x1 = x0 - f_x0 / derivative
        if not np.isfinite(x1):
            return None

        x0 = x1

    # si no convergió en max_iter, le damos solo si quedamos cerquita del 0.
    # si no, devolvemos None.
    f_end = f(x0)
    if np.isfinite(f_end) and abs(f_end) < 1e-4:
        return x0
    
    return None

# nota para mi:
# newton usa x sub n+1 = x sub n - f(x sub n) / f'(x sub n) osea que cuando f prima se hace muy chico, el paso se hace muy grande.
# segun google; si f(x sub n) es positivo, nos pasamos de la meta, hay que ajustar hacia abajo.
# si f(x sub n) es negativo, no llegamos a la meta, hay que ajustar hacia arriba.
# si f' es muy chico, el ajuste es muy grande, y puede que nos pasemos mucho de la meta.
# por eso se fuerza abs(derivative) < 1e-12 a derivative = 1e-6  (0.000001).
# NaN es Not a Number.
# el target es la nota final que queremos obtener.
# newton-raphson sirve para encontrar raíces de funciones, o sea, encontrar un valor que haga que una ecuación se cumpla.
# osea una nota que haga que la nota final sea igual al target.


def fill_empty_evals(model, empty_evals, nota):
    '''
    Llena las evaluaciones vacías con la nota proporcionada.

    :param model: Diccionario que contiene el contexto de evaluación
    :param empty_evals: Lista de índices de evaluaciones vacías
    :param nota: Nota a asignar a las evaluaciones vacías
    '''
    ctx = model['context']
    evals = np.array(ctx['values'])
    evals[empty_evals] = nota
    ctx['values'] = evals.tolist()

    out = eval_node(model['AST'], ctx)
    return out

def find_curva_nivel(model, idx_eje_x, idx_eje_y, target, n=101):
    ctx = model['context']
    evals = np.array(ctx['values'])
    
    if isinstance(idx_eje_x, (int, np.integer)):
        idx_eje_x = [int(idx_eje_x)]
    else:
        idx_eje_x = [int(i) for i in idx_eje_x]

    if isinstance(idx_eje_y, (int, np.integer)):
        idx_eje_y = [int(idx_eje_y)]
    else:
        idx_eje_y = [int(i) for i in idx_eje_y]

    # eje X en [0,100] con n puntosPara cada x fijo, resolvemos numéricamente y tal que nota_final(x, y) = target.
    xi = np.linspace(0, 100, n)

    # para cada x en xi, encontrar y tal que nota_final(x, y) = target
    yi = np.full_like(xi, np.nan, dtype=np.float64)
    x0 = target

    # iterar sobre cada x en xi
    for i, x in enumerate(xi):
        evals[idx_eje_x] = x
        ctx['values'] = evals.tolist()
        model['context'] = ctx

        # encontrar y tal que nota_final(x, y) = target
        y1 = find_nota_necesaria(model, idx_eje_y, target, x0=x0)
        # si no se encuentra, dejar NaN
        if y1 is None:
            yi[i] = np.nan
        # si se encuentra, guardarlo y usarlo como x0 para la siguiente iteración
        else:
            yi[i] = float(y1)
            x0 = float(y1)

    return xi, yi