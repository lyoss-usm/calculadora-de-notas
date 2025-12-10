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

#####################################################
############## OPERACIONES ELEMENTALES ##############
#####################################################
suma = lambda node, args, ctx: np.sum(np.array(args))
multiplicacion = lambda node, args, ctx: np.prod(np.array(args))

#####################################################
############## OPERACIONES COMPUESTAS ###############
#####################################################
mean = lambda node, args, ctx: np.mean(np.array(args))


OPS = {
    # OBTENER VALORES
    'const': const,
    'array': array,

    'ref': ref,
    'refs_by_template': refs_by_template,

    # CONDICIONAL
    'if': cond,

    'gt': gt,
    'gt_eq': gt_eq,
    
    'lt': lt,
    'lt_eq': lt_eq,

    # INDEXACIÓN
    'slice': slice,
    'sort': sort,

    # OPERACIONES ELEMENTALES
    'mul': multiplicacion,
    'add': suma,

    # OPERACIONES COMPUESTAS
    'mean': mean
}

def eval_node(node, context):
    op = node['op']
    fn = OPS[op]

    if "args" not in node:
        return fn(node, None, context)
    
    args = [eval_node(arg, context) for arg in node['args']]
    return fn(node, args, context)