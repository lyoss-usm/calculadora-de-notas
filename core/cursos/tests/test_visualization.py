import numpy as np
import pytest
from ..visualization import print_AST

# ----------------------------------------------------------------------
# Contexto base
# ----------------------------------------------------------------------

CTX = {
    "evaluations": [
        "Certamen 1",
        "Control 1",
        "Control 2",
        "Control 3",
        "Laboratorio"
    ],
    "values": [
        72.0,
        55.0,
        60.0,
        60.0,
        48.0
    ],
    "templates": {
        "certamen": [0],
        "control": [1,2,3]
    }
}

# ----------------------------------------------------------------------
# Tests de operadores primitivos
# ----------------------------------------------------------------------

def test_const():
    node = {"op": "const", "value": 3.5}
    out = print_AST(node, CTX)
    print( out )
    assert out == "3.5"

def test_array():
    node = {"op": "array", "value": [1,2,3]}
    out = print_AST(node, CTX)
    print( out )
    assert out == ["1", "2", "3"]

def test_ref():
    node = {"op": "ref", "id": 0}
    out = print_AST(node, CTX)
    print( out )
    assert out == "C_1"

def test_ref_2():
    node = {"op": "ref", "id": 4}
    out = print_AST(node, CTX)
    print( out )
    assert out == "L"

def test_refs_by_template():
    node = {"op": "ref_template", "template": "control"}
    out = print_AST(node, CTX)
    print( out )
    assert out == ["C_1", "C_2", "C_3"]

def test_add_mul_chain():
    ast = {
        "op": "sum",
        "args": [
            {"op": "prod", "args": [
                {"op":"const","value":2},
                {"op":"const","value":3}
            ]},
            {"op": "const", "value": 4}
        ]
    }
    out = print_AST(ast, CTX)
    print( out )
    assert out == "2 \\cdot 3 + 4"

# ----------------------------------------------------------------------
# Tests vectoriales
# ----------------------------------------------------------------------

def test_mean_controls():
    ast = {"op":"mean", "args":[
        {"op":"ref_template", "template":"control"}
    ]}
    out = print_AST(ast, CTX)
    print( out )
    assert out == "\\left(\\frac{C_1 + C_2 + C_3}{3}\\right)"


def test_sort_slice_best2():
    ast = {
        "op":"slice",
        "index": -2,
        "args":[
            {"op":"sort","args":[
                {"op":"ref_template","template":"control"}
            ]},
        ]
    }
    out = print_AST(ast, CTX)
    print( out )
    assert out == "(\\text{sort}(C_1, C_2, C_3))[-2:]"

# ----------------------------------------------------------------------
# Test de fórmula compuesta real
# 0.6 \cdot certamen + 0.4 \cdot mean(controles)
# ----------------------------------------------------------------------

def test_full_formula():
    ast = {
        "op":"sum",
        "args":[
            {
                "op":"prod",
                "args":[
                    {"op":"const","value":0.6},
                    {"op":"ref","id":0}
                ]
            },
            {
                "op":"prod",
                "args":[
                    {"op":"const","value":0.4},
                    {
                        "op":"mean",
                        "args":[
                            {"op":"ref_template","template":"control"}
                        ]
                    }
                ]
            }
        ]
    }
    expected = "0.6 \\cdot C_1 + 0.4 \\cdot \\left(\\frac{C_1 + C_2 + C_3}{3}\\right)"
    out = print_AST(ast, CTX)
    print( out )
    assert out == expected

# ----------------------------------------------------------------------
# Tests de comparaciones y condicional
# ----------------------------------------------------------------------

def test_conditional_then():
    ast = {
        "op":"if",
        "cond":{
            "op":"lt",
            "args":[
                {"op":"ref","id":0},
                {"op":"const","value":80}
            ]
        },
        "then":{"op":"const","value":1},
        "else":{"op":"const","value":0}
    }
    expected = "\\begin{cases} 1 & \\text{si } C_1 < 80 \\\\ 0 & \\text{en otro caso} \\end{cases}"
    out = print_AST(ast, CTX)
    print( out )
    assert out == expected

'''
'k_best': k_best,
'power': power,
'root': raiz,
'geom_mean': geometric_mean,
'''
def test_k_best():
    ast = {
        "op":"k_best",
        "k":2,
        "args":[
            {"op":"ref_template","template":"control"}
        ]
    }
    out = print_AST(ast, CTX)
    print( out )
    assert out == "\\text{best}_2(C_1, C_2, C_3)"

def test_power_root():
    ast_power = {
        "op":"power",
        "exponent":3,
        "args":[
            {"op":"ref","id":0}
        ]
    }
    out_power = print_AST(ast_power, CTX)
    print( out_power )
    assert out_power == "C_1^{3}"

    ast_root = {
        "op":"root",
        "exponent":4,
        "args":[
            {"op":"ref","id":0}
        ]
    }
    out_root = print_AST(ast_root, CTX)
    print( out_root )
    assert out_root == "\\sqrt[4]{C_1}"

def test_geometric_mean():
    ast = {
        "op":"geom_mean",
        "args":[
            {"op":"ref_template","template":"control"}
        ]
    }
    out = print_AST(ast, CTX)
    print( out )
    assert out == "\\sqrt[3]{C_1 \\cdot C_2 \\cdot C_3}"


import json

course = json.load(open("core/cursos/models/INF285.json","r"))

def test_course_full_formula():
    ast = course["AST"]
    CTX = course["context"]
    CTX['evaluations'] = course["evaluations"]
    out = print_AST(ast, CTX)
    print( out )
    expected = ""
    assert out == expected