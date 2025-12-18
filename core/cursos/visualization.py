import numpy as np

#####################################################
############ OBTENER VALORES ########################
#####################################################
const = lambda node, args, ctx: str(node['value'])
array = lambda node, args, ctx: [str(v) for v in node['value']]

def get_eval_code(eval_name):
    eval_idx = eval_name.split(' ')[-1]

    eval_code = eval_name[0]

    # Check if eval_idx is a valid index
    if eval_idx.isdigit():
        eval_code = eval_code + '_' + eval_idx

    return eval_code

def ref(node, args, ctx):
    ref_id = node['id']
    if ref_id >= len(ctx['evaluations']):
        raise ValueError(f"Referencia inválida: {ref_id}")
    
    eval_name = ctx['evaluations'][ref_id]
    
    eval_code = get_eval_code(eval_name)

    return eval_code


def refs_by_template(node, args, ctx):
    template_name = node['template']
    if template_name not in ctx['templates']:
        raise ValueError(f"Template inválido: {template_name}")
    
    indices = ctx['templates'][template_name]
    eval_names = [ctx['evaluations'][i] for i in indices]

    eval_codes = [get_eval_code(name) for name in eval_names]
    return eval_codes


#####################################################
################ CONDICIONAL ########################
#####################################################
def cond(node, args, ctx):
    cond_val = eval_node(node["cond"], ctx)
    then_val = eval_node(node["then"], ctx)
    else_val = eval_node(node["else"], ctx)

    out = "\\begin{cases} "
    out += then_val
    out += " & \\text{si } "
    out += cond_val
    out += " \\\\ "
    out += else_val
    out += " & \\text{en otro caso} \\end{cases}"

    return out
    
lt = lambda node, args, ctx: f"{args[0]} < {args[1]}"
gt = lambda node, args, ctx: f"{args[0]} > {args[1]}"
lt_eq = lambda node, args, ctx: f"{args[0]} \\le {args[1]}"
gt_eq = lambda node, args, ctx: f"{args[0]} \\ge {args[1]}"

#####################################################
################### INDEXACIÓN ######################
#####################################################
def slice(node, args, ctx):
    return "(" + ", ".join(args) + ")[" + str(node["index"]) + ":]"

def sort(node, args, ctx):
    return "\\text{sort}(" + ", ".join(args) + ")"

#####################################################
############## OPERACIONES ELEMENTALES ##############
#####################################################
def suma(node, args, ctx):
    out = " + ".join(args)
    return f"({out})"

def multiplicacion(node, args, ctx):
    out = " \\cdot ".join(args)
    return out

#####################################################
############## OPERACIONES COMPUESTAS ###############
#####################################################
def mean(node, args, ctx):
    out = " + ".join(args)
    n = str(len(args))
    return "\\left(\\frac{"+out+"}{"+n+"}\\right)"

def linear_combination(node, args, ctx):
    prods = []
    w = node['weights']
    for i in range(0, len(args)):
        prods.append(f"{w[i]} \\cdot {args[i]}")
    out = " + ".join(prods)
    return f"({out})"

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

    # OPERACIONES ELEMENTALES
    'mul': multiplicacion,
    'add': suma,

    # OPERACIONES COMPUESTAS
    'mean': mean,
    'linear_comb': linear_combination,
}

def eval_node(node, context):
    op = node['op']
    fn = OPS[op]

    if "args" not in node:
        return fn(node, None, context)
    
    args = [eval_node(arg, context) for arg in node['args']]

    # flatten args if needed
    flat_args = []
    for a in args:
        if isinstance(a, list):
            flat_args.extend(a)
        else:
            flat_args.append(a)
    args = flat_args

    return fn(node, args, context)

def print_AST(ast, context):
    out = eval_node(ast, context)

    if out[0] == '(' and out[-1] == ')':
        return out[1:-1]
    
    return out