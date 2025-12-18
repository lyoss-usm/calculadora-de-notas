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
        if abs(f_x0) < tol:
            break

        h = 1e-6
        f_x0_h = f(x0 + h)
        derivative = (f_x0_h - f_x0) / h
        
        if derivative == 0:
            derivative = 1e-6  # Evitar división por cero
        
        x1 = x0 - f_x0 / derivative
        
        x0 = x1

    return x0

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

def find_curva_nivel(model, idx_eje_x, idx_eje_y, target, n=10):
    ctx = model['context']
    evals = np.array(ctx['values'])
    print(evals)

    xi = np.linspace(0, 100, n)

    yi = np.zeros_like(xi)
    x0 = target
    for i, x in enumerate(xi):
        evals[idx_eje_x] = x
        ctx['values'] = evals.tolist()
        model['context'] = ctx
        y1 = find_nota_necesaria(model, idx_eje_y, target, x0=x0)
        yi[i] = y1
        x0 = y1

    return xi, yi