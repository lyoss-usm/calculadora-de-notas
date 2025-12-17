import numpy as np

#####################################################
############ OBTENER VALORES ########################
#####################################################
const = lambda node, args, ctx: float(node['value'])
array = lambda node, args, ctx: node['value']

ref = lambda node, args, ctx: float(ctx['values'][node['id']])

def refs_by_template(node, args, ctx):
    template_name = node['template']
    evaluation_list = ctx['templates'][template_name]

    return np.array([ctx['values'][e] for e in evaluation_list])

#####################################################
################ CONDICIONAL ########################
#####################################################
def cond(node, args, ctx):
    cond_val = eval_node(node["cond"], ctx)

    if cond_val:
        return eval_node(node["then"], ctx)
    else:
        return eval_node(node["else"], ctx)
    
lt = lambda node, args, ctx: args[0] < args[1]
gt = lambda node, args, ctx: args[0] > args[1]
lt_eq = lambda node, args, ctx: args[0] <= args[1]
gt_eq = lambda node, args, ctx: args[0] >= args[1]

#####################################################
################### INDEXACIÓN ######################
#####################################################
def slice(node, args, ctx):
    array = args[0]
    idx = int(args[1])
    if idx >= len(args):
        return []
    return array[idx:]

def sort(node, args, ctx):
    return np.sort(args[0])

def k_best(node, args, ctx):
    k = node['k']
    array = np.array(args[0])
    sorted_array = np.sort(array)[::-1]
    return sorted_array[:k]

#####################################################
############## OPERACIONES ELEMENTALES ##############
#####################################################
suma = lambda node, args, ctx: np.sum(np.array(args))
multiplicacion = lambda node, args, ctx: np.prod(np.array(args))

def power(node, args, ctx):
    if len(args) == 1:
        return np.power(args[0], node['exponent'])
    else:
        return np.power(args, node['exponent'])
    
def raiz(node, args, ctx):
    if len(args) == 1:
        return np.power(args[0], 1/node['exponent'])
    else:
        return np.power(args, 1/node['exponent'])

#####################################################
############## OPERACIONES COMPUESTAS ###############
#####################################################
mean = lambda node, args, ctx: np.mean(np.array(args))

def geometric_mean(node, args, ctx):
    product = np.prod(np.array(args))
    return product ** (1 / len(args))

def linear_combination(node, args, ctx):
    weights = np.array(node['weights'])
    values = np.array(args)
    return np.dot(weights, values)

OPS = {
    # OBTENER VALORES
    'const': const,
    'array': array,

    'ref': ref,
    'ref_template': refs_by_template,

    # CONDICIONAL
    'if': cond,

    'gt': gt,
    'gt_eq': gt_eq,
    
    'lt': lt,
    'lt_eq': lt_eq,

    # INDEXACIÓN
    'slice': slice,
    'sort': sort,
    'k_best': k_best,

    # OPERACIONES ELEMENTALES
    'mul': multiplicacion,
    'sum': suma,

    'power': power,
    'root': raiz,

    # OPERACIONES COMPUESTAS
    'mean': mean,
    'geom_mean': geometric_mean,
    'linear_comb': linear_combination,
}

def eval_node(node, context):
    '''
    Evalúa un nodo del AST de evaluación.
    
    :param node: Nodo del AST a evaluar
    :param context: Contexto de evaluación que incluye valores y plantillas
    :return: Resultado de la evaluación del nodo
    '''
    op = node['op']
    fn = OPS[op]

    if "args" not in node:
        return fn(node, None, context)
    
    args = [eval_node(arg, context) for arg in node['args']]
    return fn(node, args, context)